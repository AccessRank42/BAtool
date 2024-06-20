#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parser as p
import sys

FULL = False
DEBUG = False

def main():
    save_output = False
    A_from_CL = False
    expanded_text = False
    as_program = (False, False)
    as_program_set = False
    cleaned_args = []
    for arg in sys.argv:
        if arg == '-h':
            # print("Use: python simpl.py P_filename A_filename [output_filename]")
            print("Use: python simpl.py [-f] [-p|-l|--pp|--ll|--lp|--pl] [-h] [-t] [-c] P_filename A_filename\n")
            print("-c: interprets A_filename as a set of atoms instead of a file name, input atoms only separated by a comma, e.g. 'a,b,c,d'")
            print("-h: help; prints this text")
            print("-f: full script output; displays all failed cases")
            print("-t: expanded explanation for failure of shown case(s)")
            print("-l or --ll: input NOT as program (default); specifies input parsing behaviour")
            print("-p or --pp: input as program; specifies input parsing behaviour")
            print("--lp: P NOT as program, A as program; specifies input parsing behaviour")
            print("--pl: P as program, A NOT as program; specifies input parsing behaviour\n")
            print("'as program' input behaviour requires P resp. A to be in the format of a logic program. Simple example: 'b -> a.'")
            print("'NOT as program' input behaviour requires P to be in the format of a sequence of SE-models. Simple example: '<{x a b},{x a b}>\\n<{x a},{x a}>'")
            print("'NOT as program' input behaviour requires  A to be in the format of a set of atoms. Simple example: '{a, b, c, d}'")
            return 0
        elif arg == '-s':
            save_output = True # TODO: needs to be implemented --> but might not be needed, just use '> somefile'
        elif arg == '-c':
            A_from_CL = True
        elif arg == '-t':
            expanded_text = True
        elif arg == '-p' or arg == '--pp':
            if as_program_set:
                print('More than one input format flag set, all but the first are ignored')
                continue
            as_program = (True, True)
            as_program_set = True
        elif arg == '--pl':
            if as_program_set:
                print('More than one input format flag set, all but the first are ignored')
                continue
            as_program = (True, False)
            as_program_set = True
        elif arg == '--lp':
            if as_program_set:
                print('More than one input format flag set, all but the first are ignored')
                continue
            as_program = (False, True)
            as_program_set = True
        elif arg == '-l' or arg == '--ll':
            if as_program_set:
                print('More than one input format flag set, all but the first are ignored')
                continue
            as_program = (False, False)
            as_program_set = True
        elif arg == '-f':
            global FULL
            FULL = True
        else:
            cleaned_args.append(arg)

            
    if len(cleaned_args) < 3:
        if ((len(cleaned_args) ==  2) and A_from_CL):
            pass
        else:
            print("Please specify exactly at least a P and an A. Use with -h for usage")
            return 1
    
    try:
        SE_model_list = p.parse_SE_models_of_P(cleaned_args[1], as_program[0])
        # print(SE_model_list)
        
        if A_from_CL:
            if (len(cleaned_args) ==  2):
                A_vars = set()
            else:
                A_vars = set(cleaned_args[2].split(','))
        else:
            A_vars = p.parse_A(cleaned_args[2], as_program[1])
        # print(A_vars)
    except OSError as e:
        print("Error while parsing. Could not open file " + e.filename + ". " + e.strerror)
        return 1
    except Exception as e:
        print(e.strerror)
        print("Error while parsing. Use with -h for usage")
        return 1
    
    if DEBUG:
        print("This should be the A")
        print(A_vars)
    
    if len(SE_model_list) == 0:
        print("Program has no SE-models.")
        print("Inconsistent program.")
        
    #print(SE_model_list)
        
    if (as_program[0]):
        print_formated_SE_model_list(SE_model_list)

    projected_list = []
    for model in SE_model_list:
        projected_list.append(project_to_complement(model[0], model[1], A_vars))
    # print(projected_list)
    
    if (test_uniform_conditions(SE_model_list, A_vars)):
        print("A uniform A-simplification of P exists\n\n")
    if (test_strong_conditions(SE_model_list, A_vars)):
        print("A strong A-simplifaction of P exists")
    
def test_uniform_conditions(SE_model_list, A_vars):    
    unif_A_simp_exists = True
    print("Testing uniform simplification condition 1 ...")
    if cond_1(SE_model_list, A_vars):
        print("Condition 1 holds\n")
    else: 
        print("")
        unif_A_simp_exists = False
        
    print("Testing uniform simplification condition 2 ...")
    if cond_2(SE_model_list, A_vars):
        print("Condition 2 holds\n")
    else: 
        print("")
        unif_A_simp_exists = False
    
    print("Testing uniform simplification condition 3 ...")
    if cond_3(SE_model_list, A_vars):
        print("Condition 3 holds\n")
    else: 
        print("")
        unif_A_simp_exists = False
        
    return unif_A_simp_exists

def test_uniform_conditions_quiet(SE_model_list, A_vars):
    cond1 = cond_1(SE_model_list, A_vars, True)
    cond2 = cond_2(SE_model_list,  A_vars, True)
    cond3 = cond_3(SE_model_list, A_vars, True)
    
    # if (cond2 and not cond3):
    #     print("hey")
    #     print(A_vars)
    # if (cond3 and not cond2):
    #     print("ho")

    return cond1 and cond2 and cond3 
        

def test_strong_conditions(SE_model_list, A_vars): 
    strong_A_simp_exists = True
    print("Testing strong simplification condition 1 ...")
    if strong_cond1(SE_model_list, A_vars):
        print("Condition 1 holds\n")
    else: 
        print("")
        strong_A_simp_exists = False
        
    print("Testing strong simplification condition 2 ...")
    if strong_cond2(SE_model_list,  A_vars):
        print("Condition 2 holds\n")
    else: 
        print("")
        strong_A_simp_exists = False
    
    print("Testing strong simplification condition 3 ...")
    if strong_cond3(SE_model_list, A_vars):
        print("Condition 3 holds\n")
    else: 
        print("")
        strong_A_simp_exists = False
    
    return strong_A_simp_exists

def test_strong_conditions_quiet(SE_model_list, A_vars):
    cond1 = strong_cond1(SE_model_list, A_vars, True)
    cond2 = strong_cond2(SE_model_list,  A_vars, True)
    cond3 = strong_cond3(SE_model_list, A_vars, True)

    return cond1 and cond2 and cond3
    
def cond_1(SE_model_list, A, silent=False):
    holds = True
    for model in SE_model_list:
        X = model[0]
        Y = model[1]
        X_complement_A, Y_complement_A = project_to_complement(X, Y, A)
        if cond_1_check(SE_model_list, A, X, Y, X_complement_A, Y_complement_A):
            continue
        if not FULL:
            if not silent:
                print('Condition 1 does not hold at least for the following X, Y:')
                print(format_set(X), ',', format_set(Y))
                print("For a {X,Y} \u2208 SE(P) with X \u2282 Y, there does not exist a Y' \u2287 X such that {Y',Y'} \u2208 SE(P) and where for each M with X \u2286 M \u2282 Y, {M,Y'} \u2209 SE(P).")
            return False
        if not silent:
            print('Condition 1 does not hold for the following X, Y:')
            print(format_set(X), ',', format_set(Y))
            if holds:
                print("For a {X,Y} \u2208 SE(P) with X \u2282 Y, there does not exist a Y' \u2287 X such that {Y',Y'} \u2208 SE(P) and where for each M with X \u2286 M \u2282 Y, {M,Y'} \u2209 SE(P).")
        holds = False
    
    return holds

def cond_1_check(SE_model_list, A, X, Y, X_complement_A, Y_complement_A):
    if (not (X < Y) # X subset Y does not hold
        or (X_complement_A != Y_complement_A)): # X_{\bar{A}} = Y_{\bar{A}}
        return True    # we do not need to check further, condition holds
    valid_Y_prime_found = False
    for model_prime in SE_model_list: # search for a valid Y'
        X_prime = model_prime[0]
        Y_prime = model_prime[1]
        _, Y_prime_complement_A = project_to_complement(X_prime, Y_prime, A)
        if ((X_prime != Y_prime) # this model does not have the form <Y', Y'>
            or not (X <= Y_prime) # Y' supseteq X does not hold
            or (Y_prime_complement_A != Y_complement_A)): # Y'_{\bar{A}} = Y_{\bar{A}} does not hold
            continue # not a valid Y'
        Ms = generate_sets(X, Y_prime)
        M_failed = False
        for M in Ms:
            if (M, Y_prime) in SE_model_list: # <M, Y'> \notin SE(P) does not hold
                M_failed = True
                break
        if not M_failed:
            valid_Y_prime_found = True # this Y' is already what we were looking for ...
            break
        # ... otherwise not a valid Y', continue search
        
    if valid_Y_prime_found:
        return True # condition holds for this model <X, Y> \in SE(P)
    return False

def cond_2(SE_model_list, A, silent=False):
    holds = True
    A_subsets = generate_sets(set(), A)
    A_subsets.append(A)
    for model in SE_model_list:
        Y = model[1]
        if Y != model[0]:
            continue
        Xs = generate_sets(set(), Y)
        for X in Xs:
            Ms = generate_sets(X, Y)
            M_failed = False
            for M in Ms:
                if (M, Y) in SE_model_list: # <M, Y> \notin SE(P) does not hold
                    M_failed = True
                    break
            if M_failed:
                continue # not a valid X
                
            X_complement_A, Y_complement_A = project_to_complement(X, Y, A)
            
            for X_prime in [X_complement_A | sub_A for sub_A in A_subsets]:
                valid_Y_prime_exists = False
                for model_prime in SE_model_list:
                    Y_prime = model_prime[1]
                    
                    X_prime_complement_A, Y_prime_complement_A = project_to_complement(
                        X_prime, Y_prime, A)
                    if (Y_prime != model_prime[0] 
                        or Y_complement_A != Y_prime_complement_A
                        or not X_prime <= Y_prime):
                        continue                                    # not a valid Y'
                    
                    
                    M_primes = generate_sets(X_prime, Y_prime)
                    M_prime_failed = False
                    for M_prime in M_primes:
                        if (M_prime, Y_prime) in SE_model_list: # <M', Y'> \notin SE(P) does not hold
                            M_prime_failed = True
                            break
                    if not M_prime_failed:
                        valid_Y_prime_exists = True
                        break
                    
                if not valid_Y_prime_exists:
                    if not FULL:
                        if not silent:
                            print("Condition 2 does not hold at least for the following X, Y, X':")
                            print([format_set(X), format_set(Y), format_set(X_prime)])
                            print("For a {X,Y} with {Y,Y} \u2208 SE(P) and X \u2282 Y, such that for each M with X \u2286 M \u2282 Y, {M,Y} \u2209 SE(P) and for X',")
                            print("there does not exist a {Y',Y'} \u2208 SE(P) such that X' \u2286 Y' and for each M' with X' \u2286 M' \u2282 Y', {M',Y'} \u2209 SE(P).")   
                        return False
                    if not silent:
                        print("Condition 2 does not hold for the following X, Y, X':")
                        print([format_set(X), format_set(Y), format_set(X_prime)])
                        if holds:
                            print("For a {X,Y} with {Y,Y} \u2208 SE(P) and X \u2282 Y, such that for each M with X \u2286 M \u2282 Y, {M,Y} \u2209 SE(P) and for X',")
                            print("there does not exist a {Y',Y'} \u2208 SE(P) such that X' \u2286 Y' and for each M' with X' \u2286 M' \u2282 Y', {M',Y'} \u2209 SE(P).")  
                    holds = False
    return holds

def cond_2_check(SE_model_list, A, A_subsets, model):
    Y = model[1]
    if Y != model[0]:
        return True
    Xs = generate_sets(set(), Y)
    for X in Xs:
        Ms = generate_sets(X, Y)
        M_failed = False
        for M in Ms:
            if (M, Y) in SE_model_list: # <M, Y> \notin SE(P) does not hold
                M_failed = True
                break
        if M_failed:
            continue # not a valid X
            
        X_complement_A, Y_complement_A = project_to_complement(X, Y, A)
        
        for X_prime in [X_complement_A | sub_A for sub_A in A_subsets]:
            valid_Y_prime_exists = False
            for model_prime in SE_model_list:
                Y_prime = model_prime[1]
                
                X_prime_complement_A, Y_prime_complement_A = project_to_complement(
                    X_prime, Y_prime, A)
                if (Y_prime != model_prime[0] 
                    or Y_complement_A != Y_prime_complement_A
                    or not X_prime <= Y_prime):
                    continue                                    # not a valid Y'
                
                
                M_primes = generate_sets(X_prime, Y_prime)
                M_prime_failed = False
                for M_prime in M_primes:
                    if (M_prime, Y_prime) in SE_model_list: # <M', Y'> \notin SE(P) does not hold
                        M_prime_failed = True
                        break
                if not M_prime_failed:
                    valid_Y_prime_exists = True
                    break
                
            if not valid_Y_prime_exists:
                return False
    return True
    

def cond_3(SE_model_list, A, silent=False):
    holds = True
    for model in SE_model_list:
        X = model[0]
        Y = model[1]
        if (X != Y) or ((Y | A, Y | A) in SE_model_list):
            continue
        else:
            if not FULL:
                if not silent:
                    print('Condition 3 does not hold at least for the following Y:')
                    print(format_set(Y))
                    print('with the following Y \u222a A:')
                    print(format_set(Y | A))
                    print("The following was not satisfied: {Y,Y} \u2208 SE(P) implies {Y \u222a A, Y \u222a A} \u2208 SE(P)")
                return False
            if not silent:
                print('Condition 3 does not hold for the following Y:')
                print(format_set(Y))
                print('with the following Y \u222a A:')
                print(format_set(Y | A))
                if holds:
                    print("The following was not satisfied: {Y,Y} \u2208 SE(P) implies {Y \u222a A, Y \u222a A} \\u2208 SE(P)")
            holds = False
    return holds

def comb_uniform_conds(SE_model_list, A):
    A_subsets = generate_sets(set(), A)
    A_subsets.append(A)
    for model in SE_model_list:
        X = model[0]
        Y = model[1]
        X_complement_A, Y_complement_A = project_to_complement(X, Y, A)

        if ((cond_1_check(SE_model_list, A, X, Y, X_complement_A, Y_complement_A))      #cond 1
            and (cond_2_check(SE_model_list, A, A_subsets, model))                      #cond 2
            and ((X != Y) or ((Y | A, Y | A) in SE_model_list))):                       #cond 3
            continue
        else:
            return False
    return True

def strong_cond1(SE_model_list, A, silent=False):
    holds = True
    for model in SE_model_list:
        X = model[0]
        Y = model[1]
        if (X != Y) or (A <= Y):
            continue
        else:
            if not FULL:
                if not silent:
                    print('Strong simplification condition 1 does not hold at least for the following Y:')
                    print(format_set(Y))
                    print("The following was not satisfied: {Y,Y} \u2208 SE(P) implies A \u2286 Y")
                return False
            if not silent:
                print('Strong simplification condition 1 does not hold for the following Y:')
                print(format_set(Y))
                if holds:
                    print("The following was not satisfied: {Y,Y} \u2208 SE(P) implies A \u2286 Y")
            holds = False
    return holds

def strong_cond2(SE_model_list, A, silent=False):
    holds = True
    for model in SE_model_list:
        X = model[0]
        Y = model[1]
        X_complement_A, Y_complement_A = project_to_complement(X, Y, A)
        if (X_complement_A != Y_complement_A) or (X == Y):
            continue
        else:
            if not FULL:
                if not silent:
                    print('Strong simplification condition 2 does not hold at least for the following X, Y:')
                    print([format_set(X), format_set(Y)])
                    print("The following was not satisfied: For all {X,Y} \u2208 SE(P), X[projected to complement A] = Y[projected to complement A]  implies X = Y ")
                return False
            if not silent:
                print('Strong simplification condition 2 does not hold for the following X, Y:')
                print([format_set(X), format_set(Y)])
                if holds:
                    print("The following was not satisfied: For all {X,Y} \u2208 SE(P), X[projected to complement A] = Y[projected to complement A]  implies X = Y ")
            holds = False
    return holds

def strong_cond3(SE_model_list, A, silent=False):
    holds = True
    for model in SE_model_list:
        X = model[0]
        Y = model[1]
        if ((X | (Y & A), Y) in SE_model_list):
            continue
        else:
            if not FULL:
                if not silent:
                    print('Strong simplification condition 3 does not hold at least for the following X, Y:')
                    print([format_set(X), format_set(Y)])
                    print('with the following X \u222a (Y \u2229 A):')
                    print(format_set(X | (Y & A)))
                    print("The following was not satisfied: {X,Y} \u2208 SE(P) implies {X \u222a (Y \u2229 A), Y} \u2208 SE(P)")
                return False
            if not silent:
                print('Strong simplification condition 3 does not hold for the following X, Y:')
                print([format_set(X), format_set(Y)])
                print('with the following X \u222a (Y \u2229 A):')
                print(format_set(X | (Y & A)))
                if holds:
                    print("The following was not satisfied: {X,Y} \u2208 SE(P) implies {X \u222a (Y \u2229 A), Y} \u2208 SE(P)")
            holds = False
    return holds

def comb_strong_conds(SE_model_list, A):
    for model in SE_model_list:
        X = model[0]
        Y = model[1]
        X_complement_A, Y_complement_A = project_to_complement(X, Y, A)

        if (((X != Y) or (A <= Y))                                  #cond 1
            and ((X_complement_A != Y_complement_A) or (X == Y))    #cond 2
            and ((X | (Y & A), Y) in SE_model_list)):               #cond 3
            continue
        else:
            return False
    return True

def project(X, Y, A):
    X_A = X & A
    Y_A = Y & A
    return (X_A, Y_A)

def project_to_complement(X, Y, A):
    X_complement_A = X - A
    Y_complement_A = Y - A
    return (X_complement_A, Y_complement_A)

"""
    generates and returns a list of sets which contains the sets 
    that are supersets to subseteq and true subsets to supset
"""
def generate_sets(subseteq, supset):
    extra_elems = list(supset - subseteq)
    sets = [subseteq]
    sets.extend(gen_sets_rec(subseteq, extra_elems))
    sets.remove(supset) # this should not be necessary, fix so it doesn't get added
    return sets

def gen_sets_rec(start_set, elems):
    result = []
    for i in range(len(elems)):
        new_set = start_set | {elems[i]}
        result.append(new_set)
        result.extend(gen_sets_rec(new_set, elems[i+1:]))
    return result

def format_set(a_set):
    if len(a_set) == 0:
        return'{}'
    return a_set

def print_formated_SE_model_list(SE_model_list):
    print("The following SE models were produced from P:")
    for item in SE_model_list:
        print(item)
    print("")

# def complement(A, U):
#     A_complement = U-A #is this a valid set operation?
#     return A_complement

if __name__ == '__main__':
    main()