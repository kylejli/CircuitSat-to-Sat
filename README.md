# CircuitSat-to-Sat
CircuitSat to Sat Polyreduction. School Project

## Problem
- I wrote a Python program to polyreduce CircuitSat to Sat. 
- CircuitSat takes an input circuit and outputs “yes” if it is possible to satisfy the input circuit and “no” otherwise. 
- Sat takes input Boolean formulas  and outputs “yes” if it is possible to satisfy the input Boolean formulas and “no” otherwise

## Input/ Output
The input is an ASCII string describing a Boolean circuit. Each gate is described as Boolean equations with no spaces. Each equation is separated by a new line. The output returns “yes” if the input circuit is satisfiable, and “no” otherwise.

## Implementation
The program uses the Tseytin transformation to convert the input Boolean circuit into Boolean formulas in CNF form. It achieves this through four main steps. \
- In the first step, it converts all gates with more than three inputs to multiple gates with two inputs.
- In the second step, it converts all gates to an equivalent CNF expression as described in the textbook:

Gate	         |Equivalent CNF Expression
---------------|------------------------------------------
w1 = w2 AND w3 | (NOT w2 OR NOT w3 OR w1) AND (w2 OR NOT w1) AND (w3 OR NOT w1)
w1 = w2 OR w3	 | (w2 OR w3 OR NOT w1) AND (NOT w2 OR w1) AND (NOT w3 OR w1)
w1 = NOT w2	   | (w1 OR w2) AND (NOT w1 OR NOT w2)

(MacCormick 286)
- In the third step, all the CNF expressions from step two are combined with each other and the literal “output” using ANDs
- In the fourth step, it calls SAT with the input CNF formula to output whether the formula is satisfiable.
## Valid Polyreduction
### This program runs in polytime
1.	In step one, its runtime is O(n) since it can’t split the gates more than the number of inputs
2.	In step two, its runtime is O(n) since it converts all the gates\
    -	max 2n gates\
    -	max 6 operations per gate\
    -	12n operations = O(n)
3.	In step three, its runtime is O(n) since it just ANDs all the gates and “output”
    -	max 2n gates
    -	2n – 1 operations = O(n)
4.	In step four, its run time is O(1) since it just calls sat\
    -	sat’s runtime is not part of the polyreduction\

Add the steps together: O(n) + O(n) + O(n) + O(1)\
total: O(n) which is in polytime
### This maps Circuit Sat’s inputs to Sat’s inputs
Since the inputs will be converted to an equivalent formula, positive CircuitSat instances will be mapped to positive Sat instances and the negative CircuitSat instances will be mapped to negative Sat instances\
Circuit Sat returns yes when the input circuit has some values where the output is true. \
-	Step 1 is just splitting three or more input gates to two input gates
    -	The positive and negative instances remain the same
-	Step 2 is converting the gates to Boolean expressions
    -	each expression is true only when the gates are expressed correctly
-	Step 3 ANDs all the expressions together with “output”
    -	every expression and the output has to be true
        -	all the gates need to be expressed and the output needs to be true\

Since the circuit is equivalent to the expression, all the positive and negative instances are mapped.
