def insertion_sort(records, key):
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0 and key(records[j]) > key(current):
            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current


def binary_search(sorted_records, target_value, key):
    low = 0
    high = len(sorted_records) - 1

    while low <= high:
        mid = (low + high) // 2
        current_value = key(sorted_records[mid])

        if current_value == target_value:
            return mid

        if current_value < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def linear_search(records, target_value, key):
    for index, record in enumerate(records):
        if key(record) == target_value:
            return index

    return -1


def insertion_sort_count(records, key):
    comparisons = 0

    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if key(records[j]) <= key(current):
                break

            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current

    return comparisons


def binary_search_count(sorted_records, target_value, key):
    low = 0
    high = len(sorted_records) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        current_value = key(sorted_records[mid])

        if current_value == target_value:
            return {
                "index": mid,
                "comparison_count": comparisons
            }

        if current_value < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return {
        "index": -1,
        "comparison_count": comparisons
    }


def linear_search_count(records, target_value, key):
    comparisons = 0

    for index, record in enumerate(records):
        comparisons += 1

        if key(record) == target_value:
            return {
                "index": index,
                "comparison_count": comparisons
            }

    return {
        "index": -1,
        "comparison_count": comparisons
    }