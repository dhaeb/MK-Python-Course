#!/usr/bin/env python3

def create_freq_dict_from_word(word):
	dict_ = {}
	for letter in word:
		if letter in dict_:
			dict_[letter] = dict_[letter]+1
		else: 
			dict_[letter] = 1
	return dict_
	

def is_anagram(source, anagram):
	is_anagram = True
	dict_source = create_freq_dict_from_word(source)
	dict_anagram = create_freq_dict_from_word(anagram)
	for letter, freq in dict_source.items():
		if not letter in dict_anagram or dict_anagram[letter] < freq:
			is_anagram = False
			break
	return is_anagram

assert(is_anagram('tom', 'telephonem'))
assert(not is_anagram('all','arbitrary'))
