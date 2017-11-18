from subprocess import call as sub_call
from math import inf


free_space = '_'
user_symbol = 'o'
ai_symbol = 'x'


def clear_screen():
    sub_call('cls', shell=True)


def get_start_state():
    return [free_space] * 9


def print_state(state):
    print(' | '.join(state[:3]))
    print(' | '.join(state[3:6]))
    print(' | '.join(state[6:]))


def valid_move(move, state):
    x, y = move
    return state[x + y * 3] == free_space


def apply_move(move, state, symbol):
    x, y = move
    state[x + y * 3] = symbol
    return state


def is_draw(state):
    return all(s != free_space for s in state)


def is_winner(state, symbol):
    is_solved_group = lambda group: \
        len(set(group)) == 1 and group[0] == symbol

    return any([
        is_solved_group(state[:3]),
        is_solved_group(state[3:6]),
        is_solved_group(state[6:]),
        is_solved_group([state[(i * 3) + 0] for i in range(3)]),
        is_solved_group([state[(i * 3) + 1] for i in range(3)]),
        is_solved_group([state[(i * 3) + 2] for i in range(3)]),
        # Diagonal
        is_solved_group([state[i * 3 + i] for i in range(3)]),
        # Other diagonal
        is_solved_group([state[(i + 1) * 3 - (i + 1)] for i in range(3)])
    ])


def maxi(state):
    if is_winner(state, user_symbol):
        return 0, None
    elif is_draw(state):
        return 1, None
    elif is_winner(state, ai_symbol):
        return 2, None

    current_val, current_move = -inf, None
    for move in get_free_moves(state):
        next_state = apply_move(move, state, ai_symbol)
        mini_val, _ = mini(next_state)
        if mini_val > current_val:
            current_val = mini_val
            current_move = move

    return current_val, current_move


def mini(state):
    if is_winner(state, user_symbol):
        return 0, None
    elif is_draw(state):
        return 1, None
    elif is_winner(state, ai_symbol):
        return 2, None

    current_val, current_move = inf, None
    for move in get_free_moves(state):
        next_state = apply_move(move, state, user_symbol)
        maxi_val, _ = maxi(next_state)
        if maxi_val < current_val:
            current_val = maxi_val
            current_move = move

    return current_val, current_move


def get_free_moves(state): 
    return ((i % 3, i // 3) for i, s in enumerate(state)
            if s == free_space)


class MinmaxPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, state):
        _, move = maxi(state)
        return move


class RealPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, _):
        # return list(map(int, input().split(' ')))
        return 0, 0


if __name__ == '__main__':
    players = RealPlayer(user_symbol), MinmaxPlayer(ai_symbol)
    current_state = get_start_state()

    while not (
        is_winner(current_state, ai_symbol) or \
        is_winner(current_state, user_symbol) or \
        is_draw(current_state)
    ):
        clear_screen()
        print_state(current_state)

        current_player, _ = players
        move = current_player.get_move(current_state[::])

        if valid_move(move, current_state):
            current_state = apply_move(
                move, current_state,
                current_player.symbol
            )
            players = players[::-1]
        else:
            print('invalid move')

    _, winner = players
    print('Winner is %s' % winner)
