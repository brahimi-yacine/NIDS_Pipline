import os
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib

CLEAN_CSV = "../out/cicids_clean.csv"
MODEL_PATH = "../out/nids_pipeline.joblib"
LABEL_COL = "Label"

def main():
    # Load the cleaned CSV data
    df = pd.read_csv(CLEAN_CSV)
    print("[i] loaded:", df.shape)

    # Separate features (X) and target labels (y_text)
    X = df.drop(columns=[LABEL_COL])
    y_text = df[LABEL_COL].astype(str)

    # Encode target labels into numeric form
    le = LabelEncoder()
    y = le.fit_transform(y_text)
    print("[i] #classes:", len(le.classes_))
    print("[i] classes:", list(le.classes_)[:10], "..." if len(le.classes_) > 10 else "")

    # Build a machine learning pipeline:
    # StandardScaler -> SelectKBest -> RandomForestClassifier
    pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),  # normalize features
        ("select", SelectKBest(score_func=f_classif, k=20)),  # select top 20 features
        ("clf", RandomForestClassifier(
            n_estimators=200,  # number of trees
            random_state=42,   # for reproducibility
            n_jobs=-1          # use all CPU cores
        ))
    ])

    # Evaluate pipeline with cross-validation
    scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy", n_jobs=-1)
    print("[i] CV accuracy scores:", scores)
    print("[i] Mean accuracy:", scores.mean())

    # Train final model on the entire dataset
    pipeline.fit(X, y)

    # Ensure output directory exists and save pipeline + label encoder
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"pipeline": pipeline, "label_encoder": le}, MODEL_PATH)
    print("[+] saved model:", MODEL_PATH)

if name == "main":
    main()