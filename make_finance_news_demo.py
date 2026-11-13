"""Create a reproducible market-news stream for the classroom demo.

This is deliberately simulated: it proves the end-to-end pipeline without
claiming that generated values are live market data.  Replace the CSV adapter
in ``stream_replay.py`` with a licensed market/news feed for production use.
"""

from pathlib import Path
import numpy as np
import pandas as pd


FEATURES = ["log_return", "realised_volatility", "relative_volume", "sentiment", "sentiment_dispersion", "news_intensity"]
EVENTS = [
    (310, 355, "negative earnings surprise"),
    (720, 775, "regulatory investigation headline"),
    (1110, 1165, "unexpected positive guidance"),
]


def make_series(length: int, rng: np.random.Generator) -> np.ndarray:
    t = np.arange(length)
    returns = rng.normal(0.0002, 0.006, length)
    volatility = np.abs(rng.normal(0.012, 0.002, length))
    volume = rng.normal(1.0, 0.13, length)
    sentiment = 0.18 * np.sin(2 * np.pi * t / 90) + rng.normal(0, 0.12, length)
    dispersion = np.abs(rng.normal(0.22, 0.05, length))
    news = np.clip(rng.poisson(4, length) + rng.normal(0, 0.35, length), 0, None)
    return np.column_stack((returns, volatility, volume, sentiment, dispersion, news)).astype(np.float32)


def main() -> None:
    rng = np.random.default_rng(313)
    output = Path("dataset/FINANCE_NEWS")
    output.mkdir(parents=True, exist_ok=True)
    train = make_series(2400, rng)
    test = make_series(1500, rng)
    labels = np.zeros(len(test), dtype=np.int64)

    # Coordinated movements imitate a market-relevant news shock, not merely a price spike.
    for start, end, _ in EVENTS:
        labels[start:end] = 1
    test[310:355, 0] -= 0.030; test[310:355, 1] += 0.035; test[310:355, 2] += 1.8; test[310:355, 3] -= 1.25; test[310:355, 4] += 0.55; test[310:355, 5] += 19
    test[720:775, 0] -= 0.021; test[720:775, 1] += 0.028; test[720:775, 2] += 1.3; test[720:775, 3] -= 0.95; test[720:775, 4] += 0.42; test[720:775, 5] += 15
    test[1110:1165, 0] += 0.024; test[1110:1165, 1] += 0.020; test[1110:1165, 2] += 1.45; test[1110:1165, 3] += 1.05; test[1110:1165, 4] += 0.36; test[1110:1165, 5] += 17

    np.save(output / "FINANCE_NEWS_train.npy", train)
    np.save(output / "FINANCE_NEWS_test.npy", test)
    np.save(output / "FINANCE_NEWS_test_label.npy", labels)
    rows = pd.DataFrame(test, columns=FEATURES)
    rows.insert(0, "timestamp", pd.date_range("2026-01-05 09:30", periods=len(test), freq="min"))
    rows["event_label"] = labels
    rows.to_csv(output / "finance_news_stream.csv", index=False)
    dashboard_data = Path("web/data")
    dashboard_data.mkdir(parents=True, exist_ok=True)
    rows.to_csv(dashboard_data / "finance_news_stream.csv", index=False)
    print(f"Created {output} with events: {EVENTS}")


if __name__ == "__main__":
    main()
