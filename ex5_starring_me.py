#!/usr/bin/env python3

import string

def read_file_line_by_line(filename, action):
    source = open(filename, "rt", encoding="utf-8")
    for line in source:
        action(line)
    source.close()

def append_string_to_file(filename, line):
    with open(filename, "a", encoding="utf-8") as dest:
        dest.write("{0}\n".format(line))

read_file_line_by_line("data/pride_and_prejudice.txt", lambda line: append_string_to_file('data/starring_me.txt', line.replace('Darcy', 'Häberlein').strip()))
