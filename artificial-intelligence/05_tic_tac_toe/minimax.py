from subprocess import call as sub_call
from math import inf
from random import randrange


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


def is_valid_move(move, state):
    x, y = move
    return state[x + y * 3] == free_space


def apply_move(move, state, symbol):
    x, y = move
    new_state = state[::]
    new_state[x + y * 3] = symbol
    return new_state


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


def maxi(state, best_max=-inf, best_min=inf):
    if is_winner(state, user_symbol):
        return 0, None
    elif is_winner(state, ai_symbol):
        return 2, None
    elif is_draw(state):
        return 1, None

    current_val, current_move = -inf, None
    for move in get_free_moves(state):
        next_state = apply_move(move, state, ai_symbol)
        mini_val, _ = mini(next_state)
        if mini_val > current_val:
            current_val = mini_val
            current_move = move
        if mini_val > best_max:
            best_max = mini_val
        if mini_val > best_min:
            break

    return current_val, current_move


def mini(state, best_max=-inf, best_min=-inf):
    if is_winner(state, user_symbol):
        return 0, None
    elif is_winner(state, ai_symbol):
        return 2, None
    elif is_draw(state):
        return 1, None

    current_val, current_move = inf, None
    for move in get_free_moves(state):
        next_state = apply_move(move, state, user_symbol)
        maxi_val, _ = maxi(next_state)
        if maxi_val < current_val:
            current_val = maxi_val
            current_move = move
        if maxi_val < best_min:
            best_min = maxi_val
        if maxi_val < best_max:
            break

    return current_val, current_move


def get_free_moves(state): 
    return [(i % 3, i // 3) for i, s in enumerate(state)
            if s == free_space]


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
        return list(map(int, input().split(' ')))
        # return randrange(0, 3), randrange(0, 3)


def there_is_winner(state):
    return is_winner(current_state, ai_symbol) or \
        is_winner(current_state, user_symbol)


if __name__ == '__main__':
    players = RealPlayer(user_symbol), MinmaxPlayer(ai_symbol)
    current_state = get_start_state()

    while not (
        there_is_winner(current_state) or \
        is_draw(current_state)
    ):
        clear_screen()
        print_state(current_state)
        current_player, _ = players

        while True:
            move = get_free_moves(current_state)[0]
            if current_state.count(free_space) > 1:
                move = current_player.get_move(current_state[::])

            if is_valid_move(move, current_state):
                current_state = apply_move(
                    move, current_state,
                    current_player.symbol
                )
                players = players[::-1]
                break
            else:
                print('invalid move')

    _, winner = players
    clear_screen()
    print_state(current_state)

    if there_is_winner(current_state):
       print('winner is [%s]' % winner.symbol)
    else:
        print('draw')
