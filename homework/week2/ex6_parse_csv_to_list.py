#!/usr/bin/env python3

import sys, re

def process_csv_file(filename):
    with open(args[1], 'rt', encoding='utf-8') as source:                                                                                                                       
        return create_list_from_csv(source)

def get_all_csv_values(line):
    return list(map(lambda word: word.strip(), re.split(r',', line)))

def create_list_from_csv(iterable):
    result = []
    for line in iterable:
        result.append(get_all_csv_values(line))
    return result

assert([["name","sandra"], ["place","dl"]] == create_list_from_csv(["name,sandra    ","place,dl"]) )

args = sys.argv
argc = len(args)
if argc == 2:
    print(process_csv_file(args[1]))
else:
    print('USAGE ex6_parse_csv_to_list.py filename.csv')
