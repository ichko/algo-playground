import unittest
from n_queens import solve_n_queens, verify_solution


class NQueensTest(unittest.TestCase):

    def setUp(self):
        self.small_problems = 51
        self.big_problems = 501

    def test_small_boards(self):
        self.run_problems_of_size(self.small_problems, 25)

    def test_big_boards(self):
        self.run_problems_of_size(self.big_problems, 250)

    def run_problems_of_size(self, problems_size, size_step):
        for n in range(problems_size // 2, problems_size, size_step):
            solution = solve_n_queens(n)
            verification = verify_solution(solution)
            self.assertTrue(verification)


if __name__ == '__main__':
    unittest.main()
