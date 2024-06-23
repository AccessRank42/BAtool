#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

def main():
    pass

def parse_SE_models_of_P(filename, as_program = False):
    if as_program:
        args = ("./htmod", filename)
        completed_process = subprocess.run(args, capture_output=True, text=True)
        output = completed_process.stdout
        if output == "0\n":
            return []
    else:
        output = ''
        with open(filename) as file:
            temp = file.readline()
            while temp != '':
                output += temp
                temp =  file.readline()
    SE_model_set = set()
    for item in output.split("\n"):
        if len(item) == 0:
            continue
        X, Y = item.replace('<', '').replace('>', '').replace('{', '').replace('}', '').split(',')
        X = frozenset(x for x in X.split(' ') if x not in [''])
        Y = frozenset(x for x in Y.split(' ') if x not in [''])
        if not X <= Y: #invalid input
            print("Invalid SE-model <X, Y> provided, X <= Y does not hold with X=" + str([x for x in X]) + ", Y="+ str([y for y in Y]))
            raise
        SE_model_set.add((X, Y))
    return [(set(s[0]), set(s[1])) for s in list(SE_model_set)] #should not contain duplicates

def parse_A(filename):
    A_vars = set()
    
    text = ''
    with open(filename) as file:
        temp = file.readline()
        while temp != '':
            text += temp
            temp =  file.readline()
    A_vars = {x for x in ''.join(text.replace('{', '').replace('}', '').split()).split(',')}
    try:
        A_vars.remove('')
    except KeyError:
        pass
    return A_vars

if __name__ == '__main__':
    main()
