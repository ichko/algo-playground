from collections import defaultdict
import timeit as t
import random


def solve_n_queens(problem_size):
    return NQueens(problem_size).solve()

def verify_solution(solution):
    return solution.is_solved()


def arg_random_el(arr, el):
    return random.choice([id for id, val in enumerate(arr) if val == el])

def arg_min(arr):
    return arg_random_el(arr, min(arr))

def arg_max(arr):
    return arg_random_el(arr, max(arr))


class Column:

    def __init__(self, problem_size, x_pos):
        self.problem_size = problem_size
        self.x_pos = x_pos
        self.y_pos = random.randrange(0, problem_size)
        self.conflicts = [0 for _ in range(problem_size)]

    def get_queen_conflict(self):
        return self.conflicts[self.y_pos]

    def is_solved(self):
        return self.get_queen_conflict() <= 1

    def relocate_queen(self):
        self.y_pos = arg_min(self.conflicts)

    def update_conflict(self, y, value=1):
        self.conflicts[y] += value

    def get_conflicting_cells(self):
        result = set((x, self.y_pos) for x in range(self.problem_size))
        result.update((self.x_pos, y) for y in range(self.problem_size))

        min_coord, max_coord = min(self.x_pos, self.y_pos), \
                               max(self.x_pos, self.y_pos)
        min_inv, max_inv = min(self.problem_size - self.x_pos - 1,
                               self.y_pos), \
                           max(self.problem_size - self.x_pos - 1,
                               self.y_pos)

        x_base, y_base = self.x_pos - min_coord, self.y_pos - min_coord
        x_inv, y_inv = self.x_pos + min_inv, self.y_pos - min_inv

        result.update((x_base + i, y_base + i)
            for i in range(self.problem_size - (max_coord - min_coord)))
        result.update((x_inv - i, y_inv + i)
            for i in range(self.problem_size - (max_inv - min_inv)))

        return result

    def print_conflicts(self):
        conflicts = self.get_conflicting_cells()
        for y in range(self.problem_size):
            row = ''
            for x in range(self.problem_size):
                if x == self.x_pos and y == self.y_pos: row += 'Q '
                elif (x, y) in conflicts: row += '# '
                else: row += '- '
            print(row)


class NQueens:

    def __init__(self, problem_size):
        self.problem_size = problem_size
        self._init_board()

    def _init_board(self):
        self.board = [Column(self.problem_size, x)
                      for x in range(self.problem_size)]
        self._set_initial_conflicts()

    def is_solved(self):
        return all(c.is_solved() for c in self.board)

    def solve(self):
        max_iter = int(self.problem_size)
        current_iter = max_iter
        while True:
            if current_iter <= 0:
                self._init_board()
                current_iter = max_iter

            if not self.is_solved():
                current_iter -= 1
                # x = current_iter % self.problem_size
                # x = random.randrange(0, self.problem_size)
                x = self._get_max_conflicting_cell_id()

                old_conflicts = self.board[x].get_conflicting_cells()
                self.board[x].relocate_queen()
                new_conflicts = self.board[x].get_conflicting_cells()
                self._update_conflicts(old_conflicts, new_conflicts)
            else:
                return self
        raise Exception('no solution found')

    def _get_max_conflicting_cell_id(self):
        return arg_max([c.get_queen_conflict() for c in self.board])

    def _update_conflicts(self, old_conflicts, new_conflicts):
        for x, y in old_conflicts:
            self.board[x].update_conflict(y, -1)
        for x, y in new_conflicts:
            self.board[x].update_conflict(y, 1)

    def _set_initial_conflicts(self):
        for col in self.board:
            conflicting_cells = col.get_conflicting_cells()
            for x, y in conflicting_cells:
                self.board[x].update_conflict(y, 1)

    def print_conflicts(self):
        for y in range(self.problem_size):
            for x in range(self.problem_size):
                min_conf = min(self.board[x].conflicts)
                conflict = self.board[x].conflicts[y]
                if self.board[x].y_pos == y:
                    print(str(conflict) + '<', end='')
                else:
                    print(str(conflict) + ' ', end='')
                print('  ' if conflict != min_conf else '* ', end='')
            print()

    def print_board(self):
        for y in range(self.problem_size):
            for x in range(self.problem_size):
                print('*' if self.board[x].y_pos == y else '_', end=' ')
            print()


if __name__ == '__main__':
    problem_size = int(input())

    start_time = t.default_timer()
    solution = NQueens(problem_size).solve()
    elapsed = t.default_timer() - start_time

    solution.print_board()
    print('TIME: %.6f' % elapsed)
