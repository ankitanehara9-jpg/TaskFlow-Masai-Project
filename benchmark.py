import time

from backend.algorithms import (
    insertion_sort_count,
    linear_search_count,
    binary_search_count,
)


def make_tasks(size):
    """Create deterministic benchmark data."""
    return [
        {
            "id": i,
            "title": f"Task {i:05d}",
            "priority": (i % 5) + 1,
        }
        for i in range(1, size + 1)
    ]


def run_benchmark(size):
    tasks = make_tasks(size)

    # ==========================================================
    # INSERTION SORT
    # ==========================================================

    sort_tasks = tasks.copy()

    start = time.perf_counter()

    insertion_result = insertion_sort_count(
        sort_tasks,
        key=lambda task: task["priority"],
    )

    insertion_time = time.perf_counter() - start

    # ==========================================================
    # LINEAR SEARCH
    # ==========================================================

    start = time.perf_counter()

    linear_result = linear_search_count(
        tasks,
        f"Task {size:05d}",
        key=lambda task: task["title"].lower(),
    )

    linear_time = time.perf_counter() - start

    # ==========================================================
    # BINARY SEARCH
    # ==========================================================

    search_tasks = tasks.copy()

    search_tasks.sort(
        key=lambda task: task["title"].lower()
    )

    start = time.perf_counter()

    binary_result = binary_search_count(
        search_tasks,
        f"task {size:05d}",
        key=lambda task: task["title"].lower(),
    )

    binary_time = time.perf_counter() - start

    # ==========================================================
    # RESULTS
    # ==========================================================

    print()
    print("=" * 70)
    print(f"BENCHMARK RESULTS - {size} RECORDS")
    print("=" * 70)

    print("\nInsertion Sort:")
    print(f"  Result: {insertion_result}")
    print(f"  Time: {insertion_time:.8f} seconds")

    print("\nLinear Search:")
    print(f"  Result: {linear_result}")
    print(f"  Time: {linear_time:.8f} seconds")

    print("\nBinary Search:")
    print(f"  Result: {binary_result}")
    print(f"  Time: {binary_time:.8f} seconds")

    print("=" * 70)


# ==============================================================
# RUN ALL REQUIRED INPUT SIZES
# ==============================================================

for size in [10, 500, 3000]:
    run_benchmark(size)