import random as rand


def prob_pick(arr, key=lambda x: x):
    arr_kys = list(map(key, arr))
    arr_sum = sum(arr_kys)
    rand_pos = rand.randrange(0, arr_sum)
    cumulative_sum = 0

    for id, el in enumerate(arr):
        if cumulative_sum > rand_pos:
            return arr[id - 1]
        cumulative_sum += arr_kys[id]

    return arr[-1]


def random_dna(n):
    return [bool(rand.randrange(0, 2)) for _ in range(n)]


def crossover(left, right):
    r = rand.randrange(0, len(left))
    return left[:r] + right[r:]


def mutate(dna, mutation_prob):
    return [not g if rand.random() < mutation_prob else
            g for g in dna]


def random_population(dna_size, population_size):
    return [random_dna(dna_size) for _ in range(population_size)]


def get_dna_info(dna, items, capacity):
    value = sum(items[id].value for id, g in enumerate(dna) if g)
    weight = sum(items[id].weight for id, g in enumerate(dna) if g)
    return value if weight < capacity else 0, value, weight


def fitness(dna, items, capacity):
    return get_dna_info(dna, items, capacity)[0]


def evolve_population(old_population, items, mutation_prob, capacity):
    new_population = []
    for _ in old_population:
        left = prob_pick(old_population,
            key=lambda dna: fitness(dna, items, capacity))
        right = prob_pick(old_population,
            key=lambda dna: fitness(dna, items, capacity))
        new_population.append(mutate(crossover(left, right), mutation_prob))

    return new_population


def solve(
    items,
    capacity,
    max_iter=100,
    mutation_prob=0.05,
    population_size=50
):
    dna_size = len(items)
    population = random_population(dna_size, population_size)

    strongest = rand.choice(population)
    strongest_info = get_dna_info(strongest, items, capacity)

    while max_iter > 0:
        max_iter -= 1
        population = evolve_population(population, items, mutation_prob, capacity)
        contender = max(population,
            key=lambda dna: fitness(dna, items, capacity))

        c_fitness, c_value, c_weight = get_dna_info(contender, items, capacity)
        strongest_fitness, _, _ = strongest_info

        if c_fitness > strongest_fitness:
            strongest = contender
            strongest_info = c_fitness, c_value, c_weight

    return strongest, strongest_info


class Item:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value


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

    strongest_dna, strongest_info = solve(all_items, 5000)
    strongest_fitness, _, strongest_weight = strongest_info
    best_items = [all_items[id] for id, g in enumerate(strongest_dna) if g]

    print(', '.join(map(lambda i: i.name, best_items)))
    print('value %s, weight %s' % (strongest_fitness, strongest_weight))

    print('value of all %s, weight of all %s' %
        (combined_value, 5000))
    print('value in p %s, weight in p %s' %
        (round(strongest_fitness / combined_value * 100, 3),
         round(strongest_weight / 5000 * 100, 3)))
