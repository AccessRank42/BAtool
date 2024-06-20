#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os

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
        X, Y = item.split(", ")
        X = frozenset(x for x in X if x not in '{} <')
        Y = frozenset(x for x in Y if x not in '{} >')
        SE_model_set.add((X, Y))
    return [(set(s[0]), set(s[1])) for s in list(SE_model_set)] #should not contain duplicates

def parse_A(filename, as_program = False):
    A_vars = set()
    if as_program:
        #TODO: what is this even supposde to do?
        #TODO: figure out how to do this via subprocess (security)
        # args = ("./lp2dlp", '-F', '<'+filename+'>', 'A.out')
        # subprocess.run(args)
        # args = ('./lp2dlp','-F','<'+filename+'>','A.out')
        # subprocess.run(args)
        os.system('./lp2dlp -F <'+filename+'> A.out')
        # popen = subprocess.Popen(args)
        # popen.wait()
        with open('A.out') as file:
            first_line = file.readline()
            for var in first_line[5:-2].split(' '):
                if var.startswith('P_'): #might need to deal w/ funky atom names
                    curr_size = len(A_vars)
                    A_vars.add(var[2:])
                    if len(A_vars) > curr_size:
                        A_vars.remove(var[2:])
                        A_vars.add(var)
                else:
                    A_vars.add(var)
            # print(A_vars)
        #os.remove('A.out')
        return A_vars
    else:
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
