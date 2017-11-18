from collections import defaultdict
from random import \
    randrange as rand, \
    sample as rand_sample, \
    choice as rand_choice
import timeit as time


def solve(n):
    return NQueens(n).solve()
    
def is_solved(solution):
    return solution.is_solved()


def max_els(arr, key=lambda x: x):
    max_els = set()
    max_val = -float('inf')

    for el in arr:
        el_val = key(el)
        if max_val < el_val:
            max_els = set()
            max_els.add(el)
            max_val = el_val
        elif max_val == el_val:
            max_els.add(el)

    return max_els

def rand_max(arr, key=lambda x: x):
    return rand_sample(max_els(arr, key), 1)[0]

def rand_min(arr, key=lambda x: x):
    return rand_max(arr, key=lambda x: -key(x))


class NQueens:

    def __init__(self, n):
        self.n = n
        self._init_q()

    def solve(self):
        max_iter = self.n * 2.71 # MAGIC
        current_iter = max_iter
        while True:
            current_iter -= 1
            if current_iter <= 0:
                current_iter = max_iter
                self._init_q()
            if self.is_solved():
                return self
            else:
                q_max = rand_max(self.queens, key=lambda q: self.conflicts[q])
                q_new = self._get_new_q(q_max)

                # Make something random if the queen does not move
                # if q_max == q_new:
                    # q_max = rand_sample(self.queens, 1)[0]
                    # q_new = self._get_new_q(q_max)

                self._move_q(q_max, q_new)

    def is_solved(self):
        return all(self.conflicts[q] == 1 for q in self.queens)

    def _get_new_q(self, q_pos):
        x, _ = q_pos
        return rand_min([(x, y) for y in range(self.n) if (x, y) != q_pos],
            key=lambda q: self.conflicts[q])

    def _init_q(self):
        self.conflicts = defaultdict(lambda: 0)
        self.queens = set()

        for x in range(self.n):
            q_pos = self._get_new_q((x, 0))
            self.queens.add(q_pos)
            for pos in self._get_q_conflicts(q_pos):
                self.conflicts[pos] += 1

    def _move_q(self, q_old, q_new):
        self.queens.remove(q_old)
        self.queens.add(q_new)

        for pos in self._get_q_conflicts(q_old):
            self.conflicts[pos] -= 1
        for pos in self._get_q_conflicts(q_new):
            self.conflicts[pos] += 1

    def _get_q_conflicts(self, q_pos):
        qx, qy = q_pos

        # Horizontal and vertical lines
        result = set((x, qy) for x in range(self.n))
        result.update((qx, y) for y in range(self.n))

        min_coord, max_coord = min(qx, qy), max(qx, qy)
        min_inv, max_inv = min(self.n - qx - 1, qy), max(self.n - qx - 1, qy)

        x_base, y_base = qx - min_coord, qy - min_coord
        x_inv, y_inv = qx + min_inv, qy - min_inv

        # Diagonals
        result.update((x_base + i, y_base + i)
            for i in range(self.n - (max_coord - min_coord)))
        result.update((x_inv - i, y_inv + i)
            for i in range(self.n - (max_inv - min_inv)))

        return result

    def print_board(self):
        for y in range(self.n):
            print(' '.join(['*' if (x, y) in self.queens else '_'
                           for x in range(self.n)]))

    def print_q_conflicts(self, q_pos):
        conflicts = self._get_q_conflicts(q_pos)
        for y in range(self.n):
            print(' '.join(['*' if (x, y) == q_pos else '#'
                                if (x, y) in conflicts else '_'
                           for x in range(self.n)]))


if __name__ == '__main__':
    n = int(input())

    start_time = time.default_timer()
    print('init')
    game = NQueens(n)
    init_time = time.default_timer() - start_time
    print('init  done')
    start_time = time.default_timer()
    game.solve()
    solution_time = time.default_timer() - start_time
    print('solution found')
    # solution.print_board()
    print('init time: %.6f' % init_time)
    print('solution time: %.6f' % solution_time)
