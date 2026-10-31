"""Reproducible timing and separate peak-allocation measurements.

Run from this directory: python benchmark.py
Only standard-library modules are needed. Output defaults to results/.
"""

import argparse
import csv
import gc
import hashlib
import json
import os
import platform
import random
import statistics
import sys
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path

from sorting import merge_sort, quick_sort

ALGORITHMS = {"merge_sort": merge_sort, "quick_sort": quick_sort}


def make_inputs(size, seed):
    ascending = list(range(size))
    shuffled = ascending.copy()
    random.Random(seed + size).shuffle(shuffled)
    return {"sorted": ascending, "reverse": ascending[::-1], "random": shuffled}


def time_once(algorithm, original, expected):
    working = original.copy()  # Setup and verification are outside the timer.
    gc.collect()
    was_enabled = gc.isenabled()
    gc.disable()
    try:
        start = time.perf_counter_ns()
        algorithm(working)
        elapsed = time.perf_counter_ns() - start
    finally:
        if was_enabled:
            gc.enable()
    if working != expected:
        raise AssertionError(f"Incorrect output from {algorithm.__name__}")
    return elapsed


def memory_once(algorithm, original, expected):
    working = original.copy()  # Input storage is not part of auxiliary memory.
    gc.collect()
    tracemalloc.start()
    try:
        algorithm(working)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    if working != expected:
        raise AssertionError(f"Incorrect output from {algorithm.__name__}")
    return peak


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int,
                        default=[256, 512, 1024, 2048, 4096])
    parser.add_argument("--trials", type=int, default=7)
    parser.add_argument("--memory-trials", type=int, default=3)
    parser.add_argument("--seed", type=int, default=532)
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    if min(args.sizes) < 2 or args.trials < 1 or args.memory_trials < 1:
        parser.error("Sizes must be at least 2 and trial counts must be positive.")
    if tracemalloc.is_tracing():
        parser.error("Start Python without allocation tracing for valid timings.")
    args.output.mkdir(parents=True, exist_ok=True)
    raw, summary = [], []
    for size in args.sizes:
        expected = list(range(size))
        for kind, original in make_inputs(size, args.seed).items():
            times = {name: [] for name in ALGORITHMS}
            peaks = {name: [] for name in ALGORITHMS}
            for algorithm in ALGORITHMS.values():
                warmup = original.copy()
                algorithm(warmup)
                assert warmup == expected
            for trial in range(args.trials):
                # Alternate order to reduce a consistent first/second-run bias.
                order = list(ALGORITHMS.items())[::1 if trial % 2 == 0 else -1]
                for name, algorithm in order:
                    elapsed = time_once(algorithm, original, expected)
                    times[name].append(elapsed)
                    raw.append(dict(size=size, dataset=kind, algorithm=name,
                                    metric="time_ns", trial=trial + 1, value=elapsed))
            # Tracing overhead must never contaminate the timed runs.
            for trial in range(args.memory_trials):
                for name, algorithm in ALGORITHMS.items():
                    peak = memory_once(algorithm, original, expected)
                    peaks[name].append(peak)
                    raw.append(dict(size=size, dataset=kind, algorithm=name,
                                    metric="peak_bytes", trial=trial + 1, value=peak))
            for name in ALGORITHMS:
                summary.append(dict(size=size, dataset=kind, algorithm=name,
                                    median_ms=statistics.median(times[name]) / 1e6,
                                    min_ms=min(times[name]) / 1e6,
                                    max_ms=max(times[name]) / 1e6,
                                    median_peak_bytes=statistics.median(peaks[name])))
            print(f"Finished n={size}, {kind}", flush=True)
    script_dir = Path(__file__).resolve().parent
    metadata = {
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "implementation": platform.python_implementation(),
        "platform": platform.platform(), "machine": platform.machine(),
        "logical_cpus_visible": os.cpu_count(),
        "sizes": args.sizes, "timing_trials": args.trials,
        "memory_trials": args.memory_trials, "seed": args.seed,
        "input_generation": "distinct integers 0..n-1; Random(seed + n).shuffle",
        "timer": "perf_counter_ns; fresh copies and checks excluded; GC disabled",
        "memory": "median peak tracemalloc bytes; input excluded; separate runs; not RSS",
        "source_sha256": {name: hashlib.sha256((script_dir / name).read_bytes()).hexdigest()
                          for name in ("sorting.py", "benchmark.py")},
    }
    write_csv(args.output / "raw.csv", raw)
    write_csv(args.output / "summary.csv", summary)
    (args.output / "environment.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
