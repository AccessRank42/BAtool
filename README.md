#Simplification Tool

This tool should work for Python version 3.8+.

It consists of two parts, one that checks for a given logic program P and a set of atoms A if a strong resp. uniform A-simplification exists, the other one computes for a given logic program P all such existing A.
The former is handled by simpl.py, the latter by bfas.py.

##simpl.py

This is the main part, which checks whether or not a given set of atoms can be removed in a way as to lead to a simplified program under the equivalence notion of strong resp. uniform simplification.

For inconsistent programs (no SE-models), a message about this fact is printed and execution stops. 

Regarding the output: If a logic program was provided for P instead of a set of SE-models, the SE-models are shown first.
Afterwards, first the result of testing the uniform conditions is printed, then of testing the strong conditions. If a condition failed, a counterexample is provided.

### Usage
Use: ```python simpl.py [-f] [-p|-m] [-h] [-t] [-c] P_filename A_filename```  
e.g. 'python simpl.py p_filename a,b,c -c -p' for testing a logic program found in the file called 'p_filename' for A = {a, b, c}  
Flag explanations:\
    -c: interprets A_filename as a set of atoms instead of a file name, input atoms only separated by a comma, e.g. 'a,b,c,d' otherwise the file indicated by A_filename should in the format of a set of atoms. Simple example: '{a, b, c, d}'  
    -h: help; prints this text")  
    -f: full script output; displays all failed cases  
    -t: expanded explanation for failure of shown case(s)  
    -m: input NOT as program (default); specifies input parsing behaviour for P  
    -p: input as program; specifies input parsing behaviour for P

'as program' input behaviour requires P to be in the format of a logic program. Simple example: 'b -> a.'
'NOT as program' input behaviour requires P to be in the format of a sequence of SE-models. Simple example: '<{x a b},{x a b}>\\n<{x a},{x a}>'




##bfas.py

In order to help with the investigation of possible $A$'s for a given program $P$, a small brute force tester is also included. 


### Usage
The usage of this tester is similar to utilizing the A tester part. 

Use: ```python bfas.py [-p|-m] [-h] P_filename```  
e.g. 'python bfas.py p_filename' for finding all As of a logic program found in the file called 'p_filename'  
Flag explanations:  
    -h: help; prints e help text  
    -m: input NOT as program; specifies input parsing behaviour  
    -p: input as a logic program; specifies input parsing behaviour; default behavior
    
