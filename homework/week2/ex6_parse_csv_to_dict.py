#!/usr/bin/env python3

import sys, re

def process_csv_file(filename):
    with open(args[1], 'rt', encoding='utf-8') as source:                                                                                                                       
        return create_dict_from_csv(source)

def get_all_csv_values(line):
    return list(map(lambda word: word.strip(), re.split(r',', line)))

def create_dict_from_csv(iterable):
    result = []
    header = None
    for i, line in enumerate(iterable):
        current_line = get_all_csv_values(line)
        if i == 0:
            header = current_line
        else:
            row_dict = {}
            for j in range(0,len(header)):
                current_header = header[j]
                current_value = current_line[j]
                row_dict[current_header] = current_value
            result.append(row_dict)
    return result

expected = [{"name": "Mike", "age": "28", "profession":"scientist", "country":"Belgium"}, {"name": "Lars", "age": "49", "profession":"research director", "country":"Luxemburg"}]
result = create_dict_from_csv(["name, age, profession, country", "Mike, 28, scientist, Belgium", "Lars, 49, research director, Luxemburg"])
assert(expected == result)

args = sys.argv
argc = len(args)
if argc == 2:
    print(process_csv_file(args[1]))
else:
    print('USAGE ex6_parse_csv_to_dict.py filename.csv')
