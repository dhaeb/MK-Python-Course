#!/usr/bin/env python3

import sys, re

def process_random_text_file(filename):
    with open(args[1], 'rt', encoding='utf-8') as source:                                                                                                                       
        return create_word_set(source)

def create_word_set(iterable):
    result = set()
    for line in iterable:
        result.update(get_all_words_with_at_least_two_letters(line))
    return result

def get_all_words_with_at_least_two_letters(line):
    return re.findall(r'\S{2,}', line)

assert({"Hello", "world!", "am", "drunk!"} == create_word_set(["Hello world!", "I am drunk!"]) )

args = sys.argv
argc = len(args)
if argc == 2:
    print(process_random_text_file(args[1]))
else:
    print('USAGE ex6_ex6_get_words_with_at_least_two_chars.py filename')
