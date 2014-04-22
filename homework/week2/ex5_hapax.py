#!/usr/bin/env python3

import ex5_gutenberg_copy as m, sys

def get_hapaxes_from_file(filename, count):
    freq = m.FrequencyDict()
    m.read_file_line_by_line(filename, freq.process_line)
    return freq.get_hapaxes(count)


if len(sys.argv) == 3:
    for hapax in get_hapaxes_from_file(sys.argv[1], int(sys.argv[2])):
        print(hapax)
else: 
    print('USAGE: ex5_hapax.py filename count_hapaxes')
