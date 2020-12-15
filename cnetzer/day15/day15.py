from collections import defaultdict, deque
from itertools import islice

def two_deque():
    return deque(maxlen = 2)

def game1(numbers):
    yield None  # we want results starting with index 1, not zero
    seen = defaultdict(two_deque)
    for i,n in enumerate(numbers):
        was_first = (n not in seen)
        pos = i + 1
        seen[n].append(pos)
        yield n

    pos += 1
    while True:
        if was_first:
            n = 0
        else:
            n = seen[n][-1] - seen[n][-2]

        yield n

        was_first = (n not in seen)
        seen[n].append(pos)
        pos += 1


if __name__ == '__main__':
    import fileinput

    for line in fileinput.input():
        numbers = [int(x) for x in line.split(',')]
        print('Part 1:', list(islice(game1(numbers), 2020, 2020 + 1))[0])
        print('Part 2:', list(islice(game1(numbers), 30_000_000, 30_000_000 + 1))[0])
