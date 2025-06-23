from __future__ import annotations

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


PHASES = ["SC", "AR", "ST", "Spring", "LPS"]


def label_data(df: pd.DataFrame) -> pd.Series:
    """Assign rough Wyckoff phase labels via heuristics (placeholder)."""
    labels = [PHASES[i % len(PHASES)] for i in range(len(df))]
    return pd.Series(labels, index=df.index)


def train_model(df: pd.DataFrame) -> RandomForestClassifier:
    """Train RandomForest to classify Wyckoff phases."""
    features = df.drop(columns=["open_time", "phase"], errors="ignore")
    labels = df["phase"]
    model = RandomForestClassifier(n_estimators=200, random_state=0)
    model.fit(features, labels)
    return model


def save_model(model: RandomForestClassifier, path: str) -> None:
    joblib.dump(model, path)


def load_model(path: str) -> RandomForestClassifier:
    return joblib.load(path)


def predict(model: RandomForestClassifier, df: pd.DataFrame) -> pd.Series:
    features = df.drop(columns=["open_time"], errors="ignore")
    return pd.Series(model.predict(features), index=df.index)
