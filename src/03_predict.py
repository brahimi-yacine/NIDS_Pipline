import argparse
import pandas as pd
import joblib

DEFAULT_MODEL_PATH = "../out/nids_pipeline.joblib"


def main():
    parser = argparse.ArgumentParser(description="NIDS inference script")
    parser.add_argument("--csv", required=True, help="Path to a new CSV file for prediction")
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH, help="Path to nids_pipeline.joblib")
    parser.add_argument("--out", default=None, help="Optional output CSV file with predictions")
    args = parser.parse_args()

    bundle = joblib.load(args.model)
    pipeline = bundle["pipeline"]
    le = bundle["label_encoder"]

    df = pd.read_csv(args.csv)
    df.columns = [c.strip() for c in df.columns]

    # If input CSV contains Label column, drop it (we are predicting it)
    if "Label" in df.columns:
        df = df.drop(columns=["Label"])

    y_pred = pipeline.predict(df)
    pred_labels = le.inverse_transform(y_pred)

    print("[i] Predictions (first 20):")
    print(pred_labels[:20])

    if args.out:
        out_df = df.copy()
        out_df["PredictedLabel"] = pred_labels
        out_df.to_csv(args.out, index=False)
        print("[+] saved:", args.out)


if __name__ == "__main__":
    main()