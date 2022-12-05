import re
import sys
from pprint import pprint


def remove_comment(line):
    line = line.split('#')
    return line[0]


if __name__ == '__main__':
    # A movement file is a text file with extension '.ASC' or '.asc'
    # # and consists of a header followed by further data.
    data = """14  7  6  6 0
               1- 2 A  3- 4 B  5- 6 C  7- 8 D  9-10 E 11-12 F 13-14 A 
               6- 3 A  7- 2 B 11-13 C  9- 4 D  5- 8 E  1-10 F 14-12 B 
              12- 9 A  5-13 B  7- 4 C 11- 2 D  1- 6 E  8- 3 F 14-10 C 
               7-10 A  1- 8 B  3- 2 C  5-12 D  4-11 E  9-13 F 14- 6 D 
               4- 5 A 11-10 B  9- 8 C  1-13 D  3-12 E  6- 7 F  2-14 E 
              11- 8 A  9- 6 B  1-12 C  3-10 D 13- 7 E  2- 5 F 14- 4 F"""
    lines = data.splitlines()
    # The header is the first line of the movement and contains 5 numbers, namely: number of contestants (pairs or
    # players) number of tables number of rounds number of board groups Individual. The number Individual
    # is 0 for a pairs movement, 1 for an individual movement.

    # A comment is not allowed before the header.
    header = remove_comment(lines[0])
    assert len(header) > 0 and bool(re.match(r'^[\d ;:\-\t,]+$', header)), \
        f"The header is the first line of the movement and [should] contains 5 numbers. Found {header}"
    header_list = re.findall("\d+", header)
    pprint(header_list)
    assert len(header_list) == 5, \
        f"\"The header [...] contains 5 numbers\", found {len(header_list)} items in `{lines[0]}`"
    # @TODO Implement individual schemas
    if header_list[4] == '1':
        sys.exit('Individual schemas are not implemented yet.')
    body = lines[1:]
    for line in body:
        # After a # the rest of the line is comment.
        line = remove_comment(line)
        if line == '':
            # Also empty lines are comment.
            continue
        line = re.sub('[ \t;:,-]', '@', line.strip(' \t;:,-'))
        line = re.sub('@+', ' ', line)
        line = line.split(' ')
        print(line)
        # The contestants are indicated by consecutive numbers, starting with 1.
        # Board groups may be indicated by consecutive capital letters, starting with A, or by numbers
        # starting with 1. In one and the same movement board groups are indicated consequently,
        # either by capitals or by numbers.
        table = [[0, 0], '0']
