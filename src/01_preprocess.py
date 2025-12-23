import os, glob
import numpy as np
import pandas as pd

RAW_DIR = "../data/raw"
OUT_CLEAN = "../out/cicids_clean.csv"

DROP_COLS = ["Flow ID", "Timestamp"]
LABEL_COL = "Label"

def main():
    paths = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
    if not paths:
        raise FileNotFoundError(f"No CSV found in {RAW_DIR}")

    dfs = []
    for p in paths:
        print("[+] loading:", os.path.basename(p))
        df = pd.read_csv(p, low_memory=False)
        df.columns = [c.strip() for c in df.columns]
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    print("[i] raw shape:", df.shape)

    # remove columns
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns], errors="ignore")

    # replace inf -> nan
    df.replace([np.inf, -np.inf, "Infinity", "inf", "-inf"], np.nan, inplace=True)

    # drop rows missing label
    if LABEL_COL not in df.columns:
        raise ValueError("Label column not found")
    df = df.dropna(subset=[LABEL_COL])

    # force numeric features
    feature_cols = [c for c in df.columns if c != LABEL_COL]
    for c in feature_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # drop any remaining NaN rows
    before = df.shape[0]
    df = df.dropna(axis=0)
    print("[i] dropped NaN rows:", before - df.shape[0])

    os.makedirs(os.path.dirname(OUT_CLEAN), exist_ok=True)
    df.to_csv(OUT_CLEAN, index=False)
    print("[+] saved:", OUT_CLEAN)
    print("[i] clean shape:", df.shape)
    print("[i] top labels:\n", df[LABEL_COL].value_counts().head(10))

if __name__ == "__main__":
    main()