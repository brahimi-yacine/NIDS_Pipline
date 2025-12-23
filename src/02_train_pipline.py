"""""
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
    # 1) Load clean data
    df = pd.read_csv(CLEAN_CSV)
    print("[i] loaded:", df.shape)

    # 2) X, y
    X = df.drop(columns=[LABEL_COL])
    y_text = df[LABEL_COL].astype(str)

    # 3) LabelEncoder for y
    le = LabelEncoder()
    y = le.fit_transform(y_text)
    print("[i] #classes:", len(le.classes_))
    print("[i] classes:", list(le.classes_)[:10], "..." if len(le.classes_) > 10 else "")

    # 4) Build pipeline
    pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("select", SelectKBest(score_func=f_classif, k=20)),
        ("clf", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        ))
    ])

    # 5) Cross-validation (fast check)
    scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy", n_jobs=-1)
    print("[i] CV accuracy scores:", scores)
    print("[i] Mean accuracy:", scores.mean())

    # 6) Train final model on full data then save
    pipeline.fit(X, y)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"pipeline": pipeline, "label_encoder": le}, MODEL_PATH)
    print("[+] saved model:", MODEL_PATH)

if __name__ == "__main__":
    main()
    """
import os
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import joblib

CLEAN_CSV = "../out/cicids_clean.csv"
MODEL_PATH = "../out/nids_pipeline.joblib"
LABEL_COL = "Label"

#100000 20000
SAMPLE_SIZE = 200000

def main():
    df = pd.read_csv(CLEAN_CSV)
    print("[i] loaded:", df.shape)

    X = df.drop(columns=[LABEL_COL])
    y_text = df[LABEL_COL].astype(str)

    # LabelEncoder
    le = LabelEncoder()
    y = le.fit_transform(y_text)
    print("[i] #classes:", len(le.classes_))
    print("[i] classes:", list(le.classes_))

    #  Sample stratified labels
    if SAMPLE_SIZE < len(df):
        sss = StratifiedShuffleSplit(n_splits=1, train_size=SAMPLE_SIZE, random_state=42)
        idx, _ = next(sss.split(X, y))
        Xs = X.iloc[idx].copy()
        ys = y[idx]
        print("[i] using stratified sample:", Xs.shape)
    else:
        Xs, ys = X, y
        print("[i] using full data")

    # Pipeline
    pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("select", SelectKBest(score_func=f_classif, k=20)),
        ("clf", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        ))
    ])

    # CV  parallel  RAM
    scores = cross_val_score(pipeline, Xs, ys, cv=3, scoring="accuracy", n_jobs=1)
    print("[i] CV accuracy scores:", scores)
    print("[i] Mean accuracy:", scores.mean())

    # Train final on 
    pipeline.fit(Xs, ys)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"pipeline": pipeline, "label_encoder": le}, MODEL_PATH)
    print("[+] saved model:", MODEL_PATH)

if __name__ == "__main__":
    main()