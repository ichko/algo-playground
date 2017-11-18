from graph import Graph


class SlidingBlocks(Graph):

    def __init__(self, start):
        self.start = tuple(tuple(el for el in row) for row in start)
        cols, rows = self.get_board_shape(start)
        self.cols = cols
        self.rows = rows
        self.end = self.get_board_end(cols, rows)
        self.zero_pos_x, self.zero_pos_y = self.get_elem_pos(self.end)
        self.solution_path = []

    def solve(self):
        self.solution_path = list(self.a_star(self.start, self.end))
        solution = self.convet_path_to_moves(self.solution_path)
        return list(solution)

    def get_board_shape(self, board):
        return len(board[0]), len(board)

    def get_board_end(self, cols, rows):
        size = cols * rows
        return tuple(tuple(((r * cols) + c + 1) % size for c in range(cols))
                                                       for r in range(rows))

    def convet_path_to_moves(self, solution_path):
        for src, dst in zip(solution_path, solution_path[1:]):
            yield self.get_move_between_boards(src, dst)

    def get_neighbors(self, state):
        result = []
        x, y = self.get_elem_pos(state)

        if y > 0: result.append(self.swap(state, x, y, x, y - 1))
        if y < self.rows - 1: result.append(self.swap(state, x, y, x, y + 1))
        if x > 0: result.append(self.swap(state, x, y, x - 1, y))
        if x < self.cols - 1: result.append(self.swap(state, x, y, x + 1, y))

        return result

    def swap(self, state, src_x, src_y, dst_x, dst_y):
        new_state = [[el for el in row] for row in state]
        tmp = new_state[src_y][src_x];
        new_state[src_y][src_x] = new_state[dst_y][dst_x]
        new_state[dst_y][dst_x] = tmp

        return tuple(tuple(el for el in row) for row in new_state), \
            1 # cost of child

    def heuristic(self, current, goal):
        total = 0

        for elem in range(self.rows * self.cols - 1):
            x_cur, y_cur = self.get_elem_pos(current, elem + 1)
            x_goal, y_goal = self.get_elem_pos(goal, elem + 1)
            total = total + abs(x_cur - x_goal) + abs(y_cur - y_goal)

        return total

    def get_move_between_boards(self, src, dst):
        src_zero_x, src_zero_y = self.get_elem_pos(src)
        dst_zero_x, dst_zero_y = self.get_elem_pos(dst)
        dx, dy = src_zero_x - dst_zero_x, src_zero_y - dst_zero_y
        if dx == -1: return 'left'
        if dx == 1: return 'right'
        if dy == -1: return 'up'
        if dy == 1: return 'down'

    def get_elem_pos(self, state, elem=0):
        for y_pos in range(len(state)):
            if elem in state[y_pos]:
                return state[y_pos].index(elem), y_pos
        return -1, -1


def input_board(size):
    return [list(map(lambda n: int(n), input().split(' ')))
            for _ in range(size)]

if __name__ == '__main__':
    size = int(input())
    board = input_board(size)
    solution = SlidingBlocks(board).solve()

    print('\n'.join(solution))
