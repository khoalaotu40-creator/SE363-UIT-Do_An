"""Generate a compact multivariate anomaly-detection demo for DCdetector."""

from pathlib import Path
import numpy as np


def normal_series(length: int, channels: int, rng: np.random.Generator) -> np.ndarray:
    time = np.arange(length, dtype=np.float32)
    columns = []
    for channel in range(channels):
        period = 35 + 4 * channel
        signal = np.sin(2 * np.pi * time / period) + 0.35 * np.cos(2 * np.pi * time / (period * 2))
        columns.append(signal + rng.normal(0, 0.07, length))
    return np.stack(columns, axis=1).astype(np.float32)


def main() -> None:
    rng = np.random.default_rng(313)
    output = Path("dataset/SYNTHETIC")
    output.mkdir(parents=True, exist_ok=True)
    train = normal_series(2500, 6, rng)
    test = normal_series(1800, 6, rng)
    labels = np.zeros(len(test), dtype=np.int64)

    # Three anomaly events: spike, level shift, and oscillation disruption.
    events = [(350, 410), (900, 980), (1400, 1480)]
    for start, end in events:
        labels[start:end] = 1
    test[350:410, :3] += 3.2
    test[900:980, 2:6] -= 2.8
    test[1400:1480, :] += 1.4 * rng.normal(0, 1.0, (80, 6))

    np.save(output / "SYNTHETIC_train.npy", train)
    np.save(output / "SYNTHETIC_test.npy", test)
    np.save(output / "SYNTHETIC_test_label.npy", labels)
    print(f"Created {output} with anomaly events: {events}")


if __name__ == "__main__":
    main()
