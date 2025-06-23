import argparse

import pandas as pd

from .data import fetch_klines
from .features import compute_features
from .model import label_data, load_model, predict, save_model, train_model


def train(args: argparse.Namespace) -> None:
    df = fetch_klines(limit=args.limit)
    feat = compute_features(df)
    feat["phase"] = label_data(feat)
    feat.to_csv(args.dataset, index=False)
    model = train_model(feat)
    save_model(model, args.model)
    print(f"Model saved to {args.model}")


def run_predict(args: argparse.Namespace) -> None:
    model = load_model(args.model)
    df = fetch_klines(limit=args.limit)
    feat = compute_features(df)
    preds = predict(model, feat)
    for t, phase in zip(feat["open_time"], preds):
        print(f"{t}: {phase}")


def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Wyckoff phase detector")
    sub = p.add_subparsers(dest="cmd")

    t = sub.add_parser("train", help="Train model")
    t.add_argument("--model", default="wyckoff.pkl")
    t.add_argument("--dataset", default="wyckoff.csv")
    t.add_argument("--limit", type=int, default=500)

    pr = sub.add_parser("predict", help="Predict phases")
    pr.add_argument("--model", default="wyckoff.pkl")
    pr.add_argument("--limit", type=int, default=100)

    return p


def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()
    if args.cmd == "train":
        train(args)
    elif args.cmd == "predict":
        run_predict(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
