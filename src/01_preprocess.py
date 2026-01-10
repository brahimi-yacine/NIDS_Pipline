import os, glob
import numpy as np
import pandas as pd

RAW_DIR = "../data/raw"
OUT_CLEAN = "../out/cicids_clean.csv"

DROP_COLS = ["Flow ID", "Timestamp"]
LABEL_COL = "Label"

def main():
    # Find all CSV files in the raw data directory
    paths = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
    if not paths:
        raise FileNotFoundError(f"No CSV found in {RAW_DIR}")

    dfs = []
    for p in paths:
        # Load each CSV file into a DataFrame
        print("[+] loading:", os.path.basename(p))
        df = pd.read_csv(p, low_memory=False)
        # Remove leading/trailing spaces in column names
        df.columns = [c.strip() for c in df.columns]
        dfs.append(df)

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)
    print("[i] raw shape:", df.shape)

    # Drop unnecessary columns if present
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns], errors="ignore")

    # Replace infinite values with NaN
    df.replace([np.inf, -np.inf, "Infinity", "inf", "-inf"], np.nan, inplace=True)

    # Ensure label column exists and drop rows without label
    if LABEL_COL not in df.columns:
        raise ValueError("Label column not found")
    df = df.dropna(subset=[LABEL_COL])

    # Convert all feature columns to numeric, invalid parsing becomes NaN
    feature_cols = [c for c in df.columns if c != LABEL_COL]
    for c in feature_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Drop any remaining rows with NaN values
    before = df.shape[0]
    df = df.dropna(axis=0)
    print("[i] dropped NaN rows:", before - df.shape[0])

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUT_CLEAN), exist_ok=True)
    # Save cleaned data to CSV
    df.to_csv(OUT_CLEAN, index=False)
    print("[+] saved:", OUT_CLEAN)
    print("[i] clean shape:", df.shape)
    # Display top labels
    print("[i] top labels:\n", df[LABEL_COL].value_counts().head(10))

if __name__ == "__main__":
    main()