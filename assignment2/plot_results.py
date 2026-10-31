"""Optional charts: python -m pip install matplotlib; python plot_results.py."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    results = Path(__file__).resolve().parent / "results"
    with (results / "summary.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    plt.rcParams.update({"font.size": 11, "svg.fonttype": "none"})
    colors = {"merge_sort": "#156082", "quick_sort": "#b64d1b"}
    labels = {"merge_sort": "Merge Sort", "quick_sort": "Quick Sort"}
    for metric, ylabel, filename in (
        ("median_ms", "Median time (ms; log scale)", "timing.svg"),
        ("median_peak_bytes", "Peak traced allocation (KiB)", "memory.svg"),
    ):
        fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), layout="constrained")
        for ax, kind in zip(axes, ("sorted", "reverse", "random")):
            for name in labels:
                selected = sorted((r for r in rows if r["dataset"] == kind
                                   and r["algorithm"] == name), key=lambda r: int(r["size"]))
                factor = 1024 if metric == "median_peak_bytes" else 1
                ax.plot([int(r["size"]) for r in selected],
                        [float(r[metric]) / factor for r in selected],
                        "o-", color=colors[name], label=labels[name], linewidth=2)
            ax.set_xscale("log", base=2)
            if metric == "median_ms":
                ax.set_yscale("log")
            ax.set_title({"sorted": "Sorted", "reverse": "Reverse sorted",
                          "random": "Random"}[kind])
            sizes = sorted({int(r["size"]) for r in rows})
            ax.set_xticks(sizes, [str(n) for n in sizes], rotation=25)
            ax.set_xlabel("Number of elements")
            ax.grid(True, alpha=0.22)
            ax.spines[["top", "right"]].set_visible(False)
        axes[0].set_ylabel(ylabel)
        axes[-1].legend(frameon=False, loc="upper left")
        destination = results / filename
        fig.savefig(destination, metadata={"Date": None})
        # Normalize generated path lines for a clean text diff in version control.
        destination.write_text("\n".join(line.rstrip() for line in
                                       destination.read_text().splitlines()) + "\n")
        plt.close(fig)


if __name__ == "__main__":
    main()
