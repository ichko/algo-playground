# Uses python3

if __name__ == '__main__':
    n = int(input())
    segments = []
    for i in range(n):
        start, end = map(int, input().split())
        # subtract 0.5 so when sorted the beginnings
        # with same value as other endings are evaluated first
        segments.append((start - 5, i, 'start'))
        segments.append((end, i, 'end'))

    segments.sort(key=lambda c: c[0])

    result = []
    stack = []
    visited = set()

    for segment in segments:
        point, index, kind = segment
        if kind == 'start':
            stack.append(index)
        elif index not in visited:
            result.append(point)
            while len(stack) > 0:
                visited.add(stack.pop())

    print(len(result))
    print(' '.join(map(str, result)))
