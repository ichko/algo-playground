free_space = '_'


class MinmaxPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, state):
        pass


class UserPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, _):
        return map(int, input().split(' '))


def get_start_state():
    return ''.join([free_space] * 9)

def print_state(state):
    print(state[:3])
    print(state[3:6])
    print(state[6:])

def valid_move(state, move):
    x, y = move
    return state[x + y * 3] == free_space

def apply_move(move, state, symbol):
    x, y = move
    state[x + y * 3] = symbol
    return state

def solved(state):
    is_group_solved = lambda group: len(set(group)) == len(group)
    return all(
        is_group_solved(state[:3]),
        is_group_solved(state[3:6]),
        is_group_solved(state[6:]),
        is_group_solved([state[1]])
    )


if __name__ == '__mani__':
    players = UserPlayer('x'), MinmaxPlayer('o')
    current_state = get_start_state()

    while not solved(current_state):
        current_player, _ = players
        move = current_player.get_move(current_state)
        if valid_move(move, current_state):
            current_state = apply_move(move, current_state, current_player)
            players = players[::-1]
        else:
            print('invalid move')

    _, winner = players
    print('Winner is ' + winner)
