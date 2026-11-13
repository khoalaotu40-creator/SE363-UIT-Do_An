"""Replay a market-news feature CSV and emit human-review alerts.

This separates model scoring from action: the output is an alert for an analyst,
not an automated trading instruction.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay the financial news stream")
    parser.add_argument("--stream", default="dataset/FINANCE_NEWS/finance_news_stream.csv")
    parser.add_argument("--scores", default="result/FINANCE_NEWS_scores.npz")
    parser.add_argument("--speed", type=float, default=0, help="Seconds between alerts; 0 prints immediately")
    args = parser.parse_args()
    stream = pd.read_csv(args.stream)
    result = np.load(Path(args.scores))
    scores = result["scores"].reshape(-1)
    threshold = float(result["threshold"])
    if len(stream) != len(scores):
        raise ValueError("Stream and score lengths differ. Score this exact stream before replaying it.")

    alerts = stream.assign(anomaly_score=scores).query("anomaly_score > @threshold")
    print(f"Review threshold: {threshold:.4f}; alerts: {len(alerts)}")
    for _, row in alerts.iterrows():
        print(f"[REVIEW] {row.timestamp} score={row.anomaly_score:.4f} "
              f"sentiment={row.sentiment:+.2f} volume={row.relative_volume:.2f} "
              f"return={row.log_return:+.3%}")
        if args.speed:
            time.sleep(args.speed)


if __name__ == "__main__":
    main()
