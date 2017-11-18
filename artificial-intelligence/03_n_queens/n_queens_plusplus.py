from collections import defaultdict
from random import \
    randrange as rand, \
    sample as rand_sample, \
    choice as rand_choice, \
    shuffle as rand_shuffle
import timeit as time


def max_els(arr, key=lambda x: x):
    max_els = []
    max_val = -float('inf')

    for el in arr:
        el_val = key(el)
        if max_val < el_val:
            max_els = [el]
            max_val = el_val
        elif max_val == el_val:
            max_els.append(el)
    rand_shuffle(max_els)
    return max_els

def rand_max(arr, key=lambda x: x):
    return rand_choice(max_els(arr, key))

def rand_min(arr, key=lambda x: x):
    return rand_max(arr, key=lambda x: -key(x))


class NQueens:

    def __init__(self, n):
        self.n = n
        self._init()

    def solve(self):
        max_iter = self.n * 2.71 # MAGIC
        cur_iter = max_iter
        while True:
            cur_iter -= 1
            if cur_iter <= 0:
                print('new gen')
                cur_iter = max_iter
                self._init()
            if all(self.is_q_solved(q) for q in self.queens):
                return self
            else:
                max_q = self._get_max_q()
                new_q = self._get_new_q(max_q)
                if max_q != new_q:
                    self._move_q(max_q, new_q)

    def is_q_solved(self, q):
        return self._calc_q_conf(q) <= 3

    def _move_q(self, q_old, q_new):
        d_old, i_old, r_old = self._get_q_conflicts(q_old)
        d_new, i_new, r_new = self._get_q_conflicts(q_new)

        self.diag[d_old] -= 1
        self.i_diag[i_old] -= 1
        self.rows[r_old] -= 1

        self.diag[d_new] += 1
        self.i_diag[i_new] += 1
        self.rows[r_new] += 1

        self.queens.remove(q_old)
        self.queens.add(q_new)

    def _calc_q_conf(self, q):
        d, i, r = self._get_q_conflicts(q)
        return self.diag[d] + self.i_diag[i] + self.rows[r]

    def _get_max_q(self):
        return rand_max(self.queens, key=lambda q: self._calc_q_conf(q))

    def _get_new_q(self, q_pos):
        x, _ = q_pos
        return (x, rand_min(range(self.n),
            key=lambda y: self._calc_q_conf((x, y))))

    def _init(self):
        self.diag = [0 for _ in range(2 * self.n - 1)]
        self.i_diag = [0 for _ in range(2 * self.n - 1)]
        self.rows = [0 for _ in range(2 * self.n - 1)]
        self.queens = set()
        for x in range(self.n):
            _, y = self._get_new_q((x, 0))
            q_pos = (x, y)
            d, i, r = self._get_q_conflicts(q_pos)
            self.diag[d] += 1
            self.i_diag[i] += 1
            self.rows[r] += 1
            self.queens.add(q_pos)

    def _get_q_conflicts(self, q_pos):
        x, y = q_pos
        min_xy = min(x, y)
        min_ixy = min(self.n - x - 1, y)

        main_diag_id = (x - min_xy) + (self.n - 1) - (y - min_xy)
        sec_diag_id = (x + min_ixy) + (y - min_ixy)
        row_id = y

        return main_diag_id, sec_diag_id, row_id

    def print_board(self):
        for y in range(self.n):
            print(' '.join(['*' if (x, y) in self.queens else '_'
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
    # game.print_board()
    print('init time: %.6f' % init_time)
    print('solution time: %.6f' % solution_time)