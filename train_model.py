import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


def main():
    parser = argparse.ArgumentParser(description="Train a simple classifier.")
    parser.add_argument("csv", help="Path to CSV dataset")
    parser.add_argument("--target", required=True, help="Name of target column")
    parser.add_argument("--model-out", default="model.joblib", help="Path to save trained model")
    parser.add_argument("--test-size", type=float, default=0.2, help="Fraction of data for testing")
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    X = data.drop(columns=[args.target])
    y = data[args.target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=42)

    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Test accuracy: {acc:.3f}")

    joblib.dump(clf, args.model_out)
    print(f"Model saved to {args.model_out}")


if __name__ == "__main__":
    main()
