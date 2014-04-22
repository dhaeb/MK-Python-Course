#!/usr/bin/env python3

import sys, re


pattern = re.compile(r'(.+)?=(.+)')

def create_key_value_from_line(line):
    m = pattern.search(line)
    return (m.group(1).strip(), m.group(2).strip())

def create_dict_from_key_value(iterable):
    result_dict = {}
    for line in iterable:
        key_value = create_key_value_from_line(line)
        result_dict[key_value[0]] = key_value[1]
    return result_dict


assert({"name" : "sandra", "place" : "dl"} == create_dict_from_key_value(["name=sandra","place = dl"]) )

args = sys.argv
argc = len(args)
if argc == 2:
    with open(args[1], 'rt', encoding='utf-8') as source:
        result_dict = create_dict_from_key_value(source)
        print(result_dict)
else:
    print('USAGE ex6_create_dict.py filename')
