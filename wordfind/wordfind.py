import re
import sys
import numpy as np
import random
import enum
from collections import namedtuple


HARD = True


class Encoding(enum.Enum):
    normal = 0
    diag_up_left_to_right = 1
    up_starting_low = 2
    diag_up_right_to_left = 3
    backward = 4
    diag_down_right_to_left = 5
    down_starting_high = 6
    diag_down_left_to_right = 7


def create_wordfind(words: list, size: list):
    def choose_position():
        sz = [size[0]-1, size[1]-1]
        if direction == Encoding.normal:
            start_x = random.randint(0, sz[1] - len_word)
            start_y = random.randint(0, sz[0])
            inc_x = 1
            inc_y = 0
        elif direction == Encoding.diag_up_left_to_right:
            start_x = random.randint(0, sz[1] - len_word)
            start_y = random.randint(len_word, sz[0])
            inc_x = 1
            inc_y = -1
        elif direction == Encoding.up_starting_low:
            start_x = random.randint(0, sz[1])
            start_y = random.randint(len_word, sz[0])
            inc_x = 0
            inc_y = -1
        elif direction == Encoding.diag_up_right_to_left:
            start_x = random.randint(len_word, sz[1])
            start_y = random.randint(len_word, sz[0])
            inc_x = -1
            inc_y = -1
        elif direction == Encoding.backward:
            start_x = random.randint(len_word, sz[1])
            start_y = random.randint(0, sz[0])
            inc_x = -1
            inc_y = 0
        elif direction == Encoding.diag_down_right_to_left:
            start_x = random.randint(len_word, sz[1])
            start_y = random.randint(0, sz[0] - len_word)
            inc_x = -1
            inc_y = 1
        elif direction == Encoding.down_starting_high:
            start_x = random.randint(0, sz[1])
            start_y = random.randint(0, sz[0] - len_word)
            inc_x = 0
            inc_y = 1
        else:  # Encoding.diag_down_left_to_right
            start_x = random.randint(0, sz[1] - len_word)
            start_y = random.randint(0, sz[0] - len_word)
            inc_x = 1
            inc_y = 1
        return (start_y, start_x,), (inc_y, inc_x,)

    def place_word():
        def place():
            x = sx
            y = sy
            for letter in word:
                puzzle[y, x] = letter
                x += inc_x
                y += inc_y

        def check():
            x = sx
            y = sy
            can_place = True
            intersections = []
            inter_info = namedtuple('inter_info', ['x', 'y', 'char'])
            for letter in word:
                if puzzle[y, x] and letter != puzzle[y, x]:
                    intersections.append(inter_info(x=x, y=y, char=puzzle[y, x]))
                    can_place = False
                x += inc_x
                y += inc_y
            return can_place, intersections

        nonlocal sx, sy
        can_place, intersections = check()
        if can_place:
            # just place the word in the originally determined location
            place()
            return True
        else:
            # does the letter that already exist also exist in the current word?
            # unfortunately this happening is a low probability
            if len(intersections) == 1 and intersections[0].char in word:
                # need to adjust sx and sy to allow for correct intersection; we
                # either need to move the word forward or backward to make the
                # intersection fit
                check_sx = sx
                check_sy = sy
                ok = True
                indx = word.find(intersections[0].char)
                xx = intersections[0].x
                yy = intersections[0].y
                if inc_x == -1:
                    if xx + indx + len_word < size[1]:
                        check_sx = xx + indx
                    else:
                        ok = False
                if inc_x == 1:
                    if xx - indx >= 0 and xx - indx + len_word < size[1]:
                        check_sx = xx - indx
                    else:
                        ok = False
                if inc_y == -1:
                    if yy + indx + len_word < size[0]:
                        check_sy = yy + indx
                    else:
                        ok = False
                if inc_y == 1:
                    if yy - indx >= 0 and yy - indx + len_word < size[0]:
                        check_sy = yy - indx
                    else:
                        ok = False
                if ok:
                    sx = check_sx
                    sy = check_sy
                ok &= check()[0]
                if ok:
                    place()
                return ok
        return False

    assert len(size) == 2, ''
    assert all([len(x) <= size[0] and len(x) <= size[1] for x in words])
    puzzle = np.zeros(size, dtype=str)
    info = namedtuple('info', ['start_x', 'start_y', 'direction'])
    solution = {}
    for word in words:
        len_word = len(word)
        placed = False
        attempts = 0
        while not placed:
            assert attempts < 20000, f'could not place {word} after {attempts} attempts'
            direction = Encoding(random.randint(0, len(list(Encoding))-1))
            (sy, sx), (inc_y, inc_x) = choose_position()
            placed = place_word()
            attempts += 1
        print(f'placed {word} after {attempts} attempts')
        solution[word] = info(start_x=sx, start_y=sy, direction=direction)
        # direction = Encoding(direction.value+1)
    # hide the words by filling in gaps
    letters = set()
    for word in words:
        for letter in word:
            letters.add(letter)
    for y in range(size[0]):
        for x in range(size[1]):
            if not puzzle[y, x]:
                puzzle[y, x] = random.sample(letters, 1)[0] if HARD else chr(random.randint(ord('a'), ord('z')))

    # return the result and solution
    return puzzle, solution


def fileio(input_file, output_file):
    with open(input_file, 'r') as fid:
        words = fid.read().splitlines()
    m = re.findall(r'(\d+)x(\d+)', words[0])
    assert m, f'did not find the size of the wordfind; expected a "MxN" string on the first line of the input file ' \
              f'where "M" and "N" are numbers greater than or equal to the largest word in your list'

    size = [int(m[0][0]), int(m[0][1])]
    puzzle, solution = create_wordfind(words[1:], size)
    with open(output_file, 'w') as fid:
        # output the puzzle
        for y in range(size[0]):
            row = ''
            for x in range(size[1]):
                row += f'{puzzle[y, x]} '
            print(row, file=fid)

        # output the word list
        print(f'\nWord List:', file=fid)
        word_list = words[1:]
        word_list.sort()
        for word in word_list:
            print(word, file=fid)

        # output the solution
        print(f'\nSolution:', file=fid)
        for word, info in sorted(solution.items()):
            print(f'{word}: start (MxN): {info.start_y}x{info.start_x}, {info.direction.name}', file=fid)
    print(f'Wrote {output_file} successfully')


if __name__ == '__main__':
    # create_wordfind(words=[
    #     'candycane',
    #     'jothanan',
    #     'tree',
    #     'santa',
    #     'lights',
    #     'giving',
    #     'presents',
    #     'nativity'
    # ], size=[20, 20])
    fileio(sys.argv[1], sys.argv[2])
