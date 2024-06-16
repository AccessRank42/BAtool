#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser as p
import simpl
import sys

DEBUG = False

"""
    a brute force implementation
"""
def main():
    latex_output = False
    save_output = False
    as_program = True
    as_program_set = False
    cleaned_args = []
    for arg in sys.argv:
        if arg == '-h':
            # print("Use: python simpl.py P_filename A_filename [output_filename]")
            print("Use: python A_computer.py [-p|-l] [-h] P_filename \n")
            print("-h: help; prints this text")
            print("-latex: displays the result in a manner that makes it easier to copy into a LaTex document.")
            print("-l: input NOT as program (default); specifies input parsing behaviour")
            print("-p: input as program; specifies input parsing behaviour")
            print("'as program' input behaviour requires P resp. A to be in the format of a logic program. Simple example: 'b -> a.'")
            print("'NOT as program' input behaviour requires P to be in the format of a sequence of SE-models. Simple example: '<{x a b},{x a b}>\\n<{x a},{x a}>'")
            return 0
        elif arg == '-latex':
            latex_output = True
        elif arg == '-s':
            save_output = True # TODO: needs to be implemented --> but might not be needed, just use '> somefile'
        elif arg == '-p':
            if as_program_set:
                print('More than one input format flag set, all but the first are ignored')
                continue
            as_program = True
            as_program_set = True
        elif arg == '-l':
            if as_program_set:
                print('More than one input format flag set, all but the first are ignored')
                continue
            as_program = False
            as_program_set = True
        else:
            cleaned_args.append(arg)
            
    if len(cleaned_args) < 2: #should be 'A_computer.py' and P
        print("Please specify a P. Use with -h for usage")
        return 1
    
    try:
        SE_model_list = p.parse_SE_models_of_P(cleaned_args[1], as_program)
        # print(SE_model_list)
        
    except OSError as e:
        print("Error while parsing. Could not open file " + e.filename + ". " + e.strerror)
        return 1
    except:
        # print(e.strerror)
        print("Error while parsing. Use with -h for usage")
        return 1
    
    if len(SE_model_list) == 0:
        print("Program has no SE-models.")
        print("Inconsistent program.")
        return 0
    
    #TODO: get set of all atoms of P --> could prbly be done cheaper
    P_atoms = set()
    for model in SE_model_list:
        for set_part in model:
            for atom in set_part:
                P_atoms.add(atom)
                
    possible_As = generate_sets(set(), P_atoms) #generate subsets A' of this set
    
    # for possible_A in possible_As:  test conditions for these A', save/display those that fulfill them
    valid_uniform_As = compute_uniform_As(SE_model_list, possible_As)
    valid_strong_As = compute_strong_As(SE_model_list, possible_As)
    
    print("*" * 64)
    print("uniform As")
    if latex_output:
        print_As_for_quick_LaTex_export(valid_uniform_As)
    else:
        print_As_formated(valid_uniform_As)
    print("strong As")
    if latex_output:
        print_As_for_quick_LaTex_export(valid_strong_As)
    else:
        print_As_formated(valid_strong_As)
    

def compute_strong_As(SE_model_list, possible_As):
    valid_As = []
    for possible_A in possible_As:
        if simpl.test_strong_conditions_quiet(SE_model_list, possible_A):
            valid_As.append(possible_A)
    return valid_As 

def compute_uniform_As(SE_model_list, possible_As):
    valid_As = []
    for possible_A in possible_As:
        if simpl.test_uniform_conditions_quiet(SE_model_list, possible_A):
            valid_As.append(possible_A)
    return valid_As 

    
"""
    generates and returns a list of sets which contains the sets 
    that are supersets to subseteq and subsets to supseteq
"""
def generate_sets(subseteq, supseteq):
    extra_elems = list(supseteq - subseteq)
    sets = [subseteq]
    sets.extend(simpl.gen_sets_rec(subseteq, extra_elems))
    return sets

"""
    prints the As in a LaTex friendly manner, ommits the empty set
"""
def print_As_for_quick_LaTex_export(valid_As):
    s = ''
    for counter, A in enumerate(valid_As):
        if counter > 1:
            s = s + ', '
        if len(A) == 0:
            # s = s + '\u2205,' #prints the empty set symbol
            pass
        else:
            s = s + '\\{'
            for i, atom in enumerate(A):
                if i > 0:
                    s = s + ','
                s = s + atom
            s = s + '\\}'
    print(s)
    
"""
    prints the As in a LaTex friendly manner, displays the empty set
"""
def print_As_formated(valid_As):
    s = ''
    for counter, A in enumerate(valid_As):
        if counter > 0:
            s = s + ', '
        if len(A) == 0:
            s = s + '\u2205' #prints the empty set symbol
            # pass
        else:
            s = s + '{'
            for i, atom in enumerate(A):
                if i > 0:
                    s = s + ','
                s = s + atom
            s = s + '}'
    print(s)
    

if __name__ == '__main__':
    main()