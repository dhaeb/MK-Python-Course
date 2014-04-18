#!/usr/bin/env python3

def sum(iterable): 
    result = 0
    for entry in iterable:
        result += entry
    return result

def multiply(iterable):
    result = 1
    for entry in iterable:
        result *= entry
    return result

assert(sum([1,2,3]) == 6)
assert(multiply([3,3,3]) == 27)
