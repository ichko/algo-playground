import unittest
from random import randint, seed
from collections import defaultdict


def counting_sort_running_sum(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr

    max_item_key = max(map(key, arr))
    pos = [0] * (max_item_key + 1)
    output = [None] * len(arr)

    for item in arr:
        pos[key(item)] += 1

    for i in range(1, max_item_key + 1):
        pos[i] += pos[i - 1]

    for item in arr[::-1]:
        pos[key(item)] -= 1
        output[pos[key(item)]] = item

    return output


def counting_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr

    max_item_key = max(map(key, arr))
    counter = defaultdict(lambda: [])
    output = []

    for item in arr:
        counter[key(item)].append(item)

    for i in range(max_item_key + 1):
        output.extend(counter[i])

    return output


def radix_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr

    base = len(arr)
    max_item_key = max(map(key, arr))
    output = [(key(x), x) for x in arr]

    while max_item_key > 0:
        output = counting_sort_running_sum(output, lambda x: x[0] % base)
        output = [(x[0] // base, x[1]) for x in output]
        max_item_key //= base

    return [x[1] for x in output]


class TestSorting(unittest.TestCase):
    def test_counting_sort_running_sum(self):
        self.assert_testig_fnction(counting_sort_running_sum)

    def test_counting_sort(self):
        self.assert_testig_fnction(counting_sort)

    def test_radix_sort(self):
        self.assert_testig_fnction(radix_sort)

    def assert_testig_fnction(self, sorting_function):
        test_cases = 1000

        for i in range(test_cases):
            input_size = randint(0, 20)
            digits_size = 10
            input_arr = [randint(0, digits_size) for _ in range(input_size)]

            actual_arr = sorting_function(input_arr)
            expected_arr = sorted(input_arr)

            self.assertEqual(actual_arr, expected_arr)


if __name__ == "__main__":
    seed(4)
    unittest.main()
