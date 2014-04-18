#!/usr/bin/env python3

import sys,os

def read_file_line_by_line(filename, action):
    for line in source:
        action(line.strip())
    source.close()

def create_file_with_linenumbers(source, target):
    with open(source, "rt", encoding="utf-8") as s:
        with open(target, "wt", encoding="utf-8") as t:
            for i, line in enumerate(s):
                t.write('{0}:{1}\n'.format(i+1, line.strip()))

argc = len(sys.argv)
if argc == 2:
    file_name = sys.argv[1]
    parent = os.path.abspath(file_name +  "/../")
    create_file_with_linenumbers(file_name, "{0}/enumerated_{1}".format(parent, file_name.split("/")[-1]))
elif argc == 3:
    create_file_with_linenumbers(sys.argv[1],sys.argv[2])
else:
    print('USAGE line:_enumerator.py sourcefile [targetfile]')
    sys.exit(1)
