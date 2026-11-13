"""Plot DCdetector's anomaly scores against the ground-truth anomaly segments.

Example
-------
    .\\.venv\\Scripts\\python.exe visualize_results.py --results result/SMD_scores.npz
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def shade_anomalies(ax, labels: np.ndarray) -> None:
    """Shade each contiguous ground-truth anomaly interval once."""
    active = False
    start = 0
    for index, value in enumerate(np.r_[labels.astype(bool), False]):
        if value and not active:
            start, active = index, True
        elif active and not value:
            ax.axvspan(start, index, color="#ff6b6b", alpha=0.18, label="True anomaly")
            active = False


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize saved DCdetector scores")
    parser.add_argument("--results", required=True, help=".npz file saved by solver.py")
    parser.add_argument("--output", default=None, help="Output PNG path (default: next to .npz)")
    parser.add_argument("--start", type=int, default=0, help="First timestamp to plot")
    parser.add_argument("--length", type=int, default=3000, help="Number of timestamps to plot")
    args = parser.parse_args()

    result_path = Path(args.results)
    data = np.load(result_path)
    scores = data["scores"].reshape(-1)
    labels = data["labels"].reshape(-1).astype(int)
    threshold = float(data["threshold"])
    end = min(args.start + args.length, len(scores))
    if args.start >= end:
        raise ValueError("--start is outside the available score range")

    x = np.arange(args.start, end)
    fig, ax = plt.subplots(figsize=(15, 5))
    shade_anomalies(ax, labels[args.start:end])
    ax.plot(x, scores[args.start:end], color="#1769aa", lw=1.15, label="Market-news anomaly score")
    ax.axhline(threshold, color="#d32f2f", ls="--", lw=1.4, label=f"Threshold = {threshold:.4g}")
    ax.set(title="Market-news monitor: anomaly score versus verified events", xlabel="Time step", ylabel="Anomaly score")
    handles, labels_ = ax.get_legend_handles_labels()
    by_label = dict(zip(labels_, handles))
    ax.legend(by_label.values(), by_label.keys(), loc="upper right")
    ax.grid(alpha=0.2)
    fig.tight_layout()

    output = Path(args.output) if args.output else result_path.with_name(result_path.stem + "_plot.png")
    fig.savefig(output, dpi=180)
    print(f"Saved plot to {output}")


if __name__ == "__main__":
    main()
