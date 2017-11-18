from random import \
    randrange as rand, \
    sample as rand_sample, \
    choice as rand_choice, \
    shuffle as rand_shuffle
import timeit as time


n = 50
diagonal = [0 for _ in range(2 * n - 1)]
sce_diagonal = [0 for _ in range(2 * n - 1)]
queens = [x for x in range(n)]

def init():
    x = 0
    for _ in range(int(n * 3.08)):
        r = rand(x, n)
        swap(x, r)
        if partial_collisions(x) == 0: x += 1
        else: swap(x, r)
    for qx in range(x, n)
        r = rand(qx, n)
        swap(qx, r)
    return x

def search(x):
    for _ in range(x, n):
        if sum(qx for qx in queens) != 0:
            pass

def partial_collisions(x):
    md, sd = get_diag(x, queens[x])
    return diagonal[md] + sec_diagonal[sd]

def get_diag(x, y):
    return n // 2 + 1 + x - y, x + y

def swap(lx, rx):
    ly, ry = queens[lx], queens[rx]
    queens[lx], queens[rx] = queens[rx], queens[lx]

    lmd_old, lsd_old = get_diag(lx, ly)
    rmd_old, rsd_old = get_diag(rx, ry)

    lmd_new, lsd_new = get_diag(lx, ry)
    rmd_new, rsd_new = get_diag(rx, ly)

    diagonal[lmd_old] -= 1
    sec_diagonal[lsd_old] -= 1
    diagonal[rmd_old] -= 1
    sec_diagonal[rsd_old] -= 1

    diagonal[lmd_new] += 1
    sec_diagonal[lsd_new] += 1
    diagonal[rmd_new] += 1
    sec_diagonal[rsd_new] += 1


x = init()

print(queens)
