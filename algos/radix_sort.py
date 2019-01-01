import unittest
from random import randint
from collections import defaultdict


def counting_sort(arr, key=lambda x: x):
    if len(arr) == 0:
        return []

    max_item_key = max(map(key, arr))
    counter = defaultdict(lambda: [])
    output = []

    for item in arr:
        counter[key(item)].append(item)

    for i in range(max_item_key + 1):
        output.extend(counter[i])

    return output


def radix_sort(arr):
    return arr


class TestSorting(unittest.TestCase):
    def test_counting_sort(self):
        self.assert_testig_fnction(counting_sort)

    def assert_testig_fnction(self, sorting_function):
        test_cases = 100

        for i in range(test_cases):
            input_size = randint(0, 20)
            digits_size = 100
            input_arr = [randint(0, digits_size) for _ in range(input_size)]

            actual_arr = sorting_function(input_arr)
            expected_arr = sorted(input_arr)

            self.assertEqual(actual_arr, expected_arr)


if __name__ == "__main__":
    unittest.main()
