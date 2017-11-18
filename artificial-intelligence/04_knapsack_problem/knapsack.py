from random import \
    randrange as rand, \
    choice as rand_choice, \
    sample
from math import sqrt


def rand_sample(set_collection):
    return sample(set_collection, 1)[0]

def prob_choice(set_collection, key=lambda x: x, revert=False):
    arr_sum = sum(map(key, set_collection))
    rand_pos = rand(0, arr_sum + 1)
    cur_sum = 0
    for el in set_collection:
        if cur_sum > rand_pos:
            return el
        el_key = key(el)
        cur_sum += el_key if not revert else arr_sum - el_key
    return rand_sample(set_collection)

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
    # rand_shuffle(max_els)
    return max_els

def rand_max(arr, key=lambda x: x):
    return rand_choice(max_els(arr, key))

def rand_min(arr, key=lambda x: x):
    return rand_max(arr, key=lambda x: -key(x))


class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


class Knapsack:
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity
        self.max_iter = 40
        self.n = len(items)

        self.population_size = 50
        self.mutation_rate = 0.5
        self.population = set(self._random_dna()
                              for _ in range(self.population_size))

        self.best_dna = rand_sample(self.population)

    def run(self):
        cur_iter = self.max_iter
        while cur_iter > 0:
            cur_iter -= 1
            strong_dna = set()
            weak_dna = set()

            for _ in range(1):
                left_parent = self._get_strong_dna()
                right_parent = self._get_strong_dna()

                strong_dna.add(
                    self._mutate(self._crossover(left_parent, right_parent))
                )
                weak_dna.add(self._get_weak_dna())

            for dna in weak_dna:
                self.population.discard(dna)
            for dna in strong_dna:
                self.population.add(dna)

            strongest_dna = max(strong_dna, key=self._fitness)
            print(self._fitness(self._get_weak_dna()), self._fitness(self._get_strong_dna()))
            if self._fitness(self.best_dna) < self._fitness(strongest_dna):
                self.best_dna = strongest_dna

        return self

    def get_solution(self):
        value, weight = self._get_dna_info(self.best_dna)
        return [self.items[id] for id, gene
                in enumerate(self.best_dna) if gene], value, weight

    def _mutate(self, dna):
        r = rand(0, 100) / 100
        dna = [not gene if r < self.mutation_rate else gene for gene in dna]
        while self._fitness(dna) <= 0:
            r_gene = rand(0, self.n)
            dna[r_gene] = False
        return tuple(dna)

    def _crossover(self, l, r):
        dna = [False for _ in range(self.n)]
        for gene_id in range(self.n):
            parent_rand = rand(0, 2)
            gene_val = (l, r)[parent_rand][gene_id]
            if gene_val:
                dna[gene_id] = gene_val
                _, weight = self._get_dna_info(dna)
                if weight > self.capacity:
                    dna[gene_id] = False
                    break

        return dna

    def _get_strong_dna(self):
        return max(self.population,
            key=lambda dna: self._fitness(dna))

    def _get_weak_dna(self):
        return min(self.population,
            key=lambda dna: self._fitness(dna))

    def _get_dna_info(self, dna):
        a = 5
        value = sum(self.items[id].value for id, gene in enumerate(dna) if gene)
        weight = sum(self.items[id].weight for id, gene in enumerate(dna) if gene)
        return value, weight

    def _fitness(self, dna):
        value, weight = self._get_dna_info(dna)
        return 0 if weight > self.capacity else max(int(value), 0)

    def _random_dna(self):
        dna = [True for _ in range(self.n)]
        genes = set(range(self.n))
        while self._fitness(dna) <= 0:
            gene = rand_sample(genes)
            genes.remove(gene)
            dna[gene] = False
        return tuple(dna)


if __name__ == '__main__':
    all_items = [
        Item('map', 90, 150),
        Item('compass', 130, 35),
        Item('water', 1530, 200),
        Item('sandwich', 500, 160),
        Item('glucose', 150, 60),
        Item('tin', 680, 45),
        Item('banana', 270, 60),
        Item('apple', 390, 40),
        Item('cheese', 230, 30),
        Item('beer', 520, 10),
        Item('suntan cream', 110, 70),
        Item('camera', 320, 30),
        Item('T-shirt', 240, 15),
        Item('trousers', 480, 10),
        Item('umbrella', 730, 40),
        Item('waterproof trousers', 420, 70),
        Item('waterproof overclothes', 430, 75),
        Item('note-case', 220, 80),
        Item('sunglasses', 70, 20),
        Item('towel', 180, 12),
        Item('socks', 40, 50),
        Item('book', 300, 10),
        Item('notebook', 900, 1),
        Item('tent', 2000, 150)
    ]
    combined_value = sum(item.value for item in all_items)
    combined_weight = sum(item.weight for item in all_items)

    knapsack = Knapsack(all_items, 5000).run()
    best_items, value, weight = knapsack.get_solution()

    print(', '.join(map(lambda i: i.name, best_items)))
    print('value %s, weight %s' % (value, weight))

    print('value of all %s, weight of all %s' %
        (combined_value, 5000))
    print('value in p %s, weight in p %s' %
        (round(value / combined_value * 100, 3), round(weight / 5000 * 100, 3)))
