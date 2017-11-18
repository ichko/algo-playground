import time


# Helpers
def generate_start_and_end(n):
    return (('>' * n) + '_' + ('<' * n),
        ('<' * n) + '_' + ('>' * n))


# Algorithm
def next_positions(position):
    return set(
        valid_pos for valid_pos in [
            position.replace('_<', '<_'), position.replace('>_', '_>'),
            position.replace('><_', '_<>'),  position.replace('>>_', '_>>'),
            position.replace('_><', '<>_'), position.replace('_<<', '<<_')
        ] if valid_pos != position
    )

def find_path(start, end, next_positions):
    visited = set()
    path = []

    def dfs(current):
        visited.add(current)
        if current == end:
            return True
        for child in next_positions(current):
            if child not in visited and dfs(child):
                path.append(child)
                return True
        return False

    if dfs(start):
        return [start] + path[::-1]


# Solver
def solve(n):
    start, end = generate_start_and_end(n)
    return find_path(start, end, next_positions)


# Test time execution
for n in range(0, 21):
    start_time = time.time()
    path = solve(n)
    execution_time = time.time() - start_time
    print('inp {}\ttime {:0.5f}s,\tpath len {}'.format(
        n, execution_time, len(path)))


n = int(input())
path = solve(n)
print('\n'.join(path))

