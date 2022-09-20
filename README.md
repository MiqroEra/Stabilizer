# Stabilizer
A tool for finding & sorting the HF stabilizers

## Install
Since this is a simple python file, just include it directly in $PYTHONPATH.

## Dependency
Need Numpy package

## How to Use
``` python
from stabilizer import stabilizer

hf = stabilizer(p)
# p is the path or qiskit tensor object
hf.run()
```
The pauli operators is stored in a sorted "quaternary tree" (like binary tree) so that when a stabilizer is found, the number of term decrease as $log_4N$.

See more details in the examples
