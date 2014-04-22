#!/usr/bin/env python3

import string

def read_file_line_by_line(filename, action):
    source = open(filename, "rt", encoding="utf-8")
    for line in source:
        action(line)
    source.close()

class FrequencyDict(object):
    def __init__(self):
        self.__dict = {}

    def process_line(self, line):
        filtered_line = filter(lambda word: word not in string.punctuation, line.lower().split(" "))
        words = list(map(lambda word: self.__add_to_dict(self.__remove_all(word.strip(), string.punctuation)), filtered_line))

    def __remove_all(self, word, removable):
        for char in removable:
            word = word.replace(char, "")
        return word

    def __add_to_dict(self, word):
        if word in self.__dict:
            self.__dict[word] = self.__dict[word] + 1
        else:
            self.__dict[word] = 1

    def get_dict(self):
        return self.__dict

    def get_hapaxes(self, occurence = 1):
        hapax_dict = dict((k, v) for k, v in self.__dict.items() if v == occurence)
        return hapax_dict.keys()

if __name__ == "main":
    freq = FrequencyDict()
    read_file_line_by_line("data/pride_and_prejudice.txt", freq.process_line)
    dict_ = freq.get_dict()
    dest = open("data/frequencies.txt", "wt", encoding="utf-8")
    for word in sorted(dict_, key=dict_.get, reverse=True):
        dest.write("{0}:{1}\n".format(word, dict_[word]))
    dest.close()
    print('script finished')
