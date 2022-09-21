# Stabilizer
![微信图片_20220920130336](https://user-images.githubusercontent.com/55620073/191171772-d1c0c606-10ef-4cdd-bbfd-4f5a1a3f6ed2.png)
A tool for finding & sorting the HF stabilizers

## Install
Since this is a simple python file, just include it directly in $PYTHONPATH.

## Dependency
Need Numpy package

## How to Use
``` python
from stabilizer import hf

myhf = hf(p) # p is the path or qiskit tensor object
myhf.run() # Predict the states
# now the tool can not deal with entangled states 
# only core and vacuum orbitals could be fill.

myhf2 = hf(p)
myhf2.
```
The pauli operators is stored in a sorted "quaternary tree" (like binary tree) so that when a stabilizer is found, the number of term decrease as $log_4N$.

See more details in the examples
