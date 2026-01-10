import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report


CLEAN_CSV = "../out/cicids_clean.csv"
MODEL_PATH = "../out/nids_pipeline.joblib"
REPORT_PATH = "../reports/metrics_report.txt"
LABEL_COL = "Label"


MAX_ROWS_TRAIN = 300_000   
CV_FOLDS = 3              
N_JOBS = 1                
N_ESTIMATORS = 100        


def main():
    df = pd.read_csv(CLEAN_CSV)
    print("[i] loaded:", df.shape)

    # Optional sampling for training speed/memory
    if len(df) > MAX_ROWS_TRAIN:
        df = df.sample(n=MAX_ROWS_TRAIN, random_state=42)
        print("[i] sampled to:", df.shape)

    if LABEL_COL not in df.columns:
        raise ValueError("Label column not found in cleaned CSV")

    X = df.drop(columns=[LABEL_COL])
    y_text = df[LABEL_COL].astype(str)

    le = LabelEncoder()
    y = le.fit_transform(y_text)
    print("[i] #classes:", len(le.classes_))
    print("[i] classes (first 15):", list(le.classes_)[:15])

    pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("select", SelectKBest(score_func=f_classif, k=20)),
        ("clf", RandomForestClassifier(
            n_estimators=N_ESTIMATORS,
            random_state=42,
            n_jobs=N_JOBS
        ))
    ])

    # Cross-validation accuracy (required)
    scores = cross_val_score(
        pipeline, X, y,
        cv=CV_FOLDS,
        scoring="accuracy",
        n_jobs=N_JOBS
    )
    print("[i] CV accuracy scores:", scores)
    print("[i] Mean accuracy:", scores.mean())

    # Train/test split to get per-class metrics (precision/recall/F1)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    labels = list(range(len(le.classes_)))
    report = classification_report(
        y_test, y_pred,
        labels=labels,
        target_names=le.classes_,
        digits=4,
        zero_division=0
    )

    print(report)

    # Save report
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(f"CV folds: {CV_FOLDS}\n")
        f.write(f"CV mean accuracy: {scores.mean():.6f}\n\n")
        f.write(report)
    print("[+] saved report:", REPORT_PATH)

    # Train final model on all sampled data and save
    pipeline.fit(X, y)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"pipeline": pipeline, "label_encoder": le}, MODEL_PATH)
    print("[+] saved model:", MODEL_PATH)


if __name__ == "__main__":
    main()