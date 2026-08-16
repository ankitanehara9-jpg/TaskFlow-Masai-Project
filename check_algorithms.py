from backend.algorithms import (
    insertion_sort,
    linear_search,
    binary_search,
    insertion_sort_count,
    linear_search_count,
    binary_search_count,
)


tasks = [
    {"id": 1, "title": "Python", "priority": 3},
    {"id": 2, "title": "HTML", "priority": 1},
    {"id": 3, "title": "JavaScript", "priority": 2},
]


# -----------------------------
# Insertion Sort
# -----------------------------
sorted_tasks = tasks.copy()

insertion_sort(
    sorted_tasks,
    key=lambda task: task["priority"]
)

print("Insertion Sort:")
print(sorted_tasks)

insertion_comparisons = insertion_sort_count(
    tasks.copy(),
    key=lambda task: task["priority"]
)

print("Comparisons:", insertion_comparisons)


# -----------------------------
# Linear Search
# -----------------------------
linear_result = linear_search(
    tasks,
    "html",
    key=lambda task: task["title"].lower()
)

print("\nLinear Search:")
print("Index:", linear_result)

linear_count_result = linear_search_count(
    tasks,
    "html",
    key=lambda task: task["title"].lower()
)

print("Count Result:", linear_count_result)


# -----------------------------
# Binary Search
# -----------------------------
search_tasks = sorted(
    tasks,
    key=lambda task: task["title"].lower()
)

binary_result = binary_search(
    search_tasks,
    "javascript",
    key=lambda task: task["title"].lower()
)

print("\nBinary Search:")
print("Index:", binary_result)

binary_count_result = binary_search_count(
    search_tasks,
    "javascript",
    key=lambda task: task["title"].lower()
)

print("Count Result:", binary_count_result)


# -----------------------------
# PASS checks
# -----------------------------
assert [task["priority"] for task in sorted_tasks] == [1, 2, 3]
assert linear_result == 1
assert binary_result != -1

assert insertion_comparisons >= 0
assert linear_count_result["comparison_count"] >= 1
assert binary_count_result["comparison_count"] >= 1

assert set(binary_count_result.keys()) == {
    "index",
    "comparison_count",
}

assert set(linear_count_result.keys()) == {
    "index",
    "comparison_count",
}

print("\nALL ALGORITHM CHECKS PASSED")