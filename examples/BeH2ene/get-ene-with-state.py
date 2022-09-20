from stabilizer import *

def prtrans(states):
    mps = []
    for i in states:
        k = 1 if i == 0 else -1
        mps.append(k)
    return mps

p = 'BeH2-1.32.txt'
hf = hf(p)
states = [0,0,0,0,1,0,1,1,1,1,0,1]
eigenvalues = prtrans(states)
print(eigenvalues)
print('The basic energy:', hf.data[0])
for idx, i in enumerate(eigenvalues):
    qbit = (idx, 'Z')
    hf.treefold(qbit, 'I', i)
    hf.flush_operators()
    print('system energy:', hf.data[0])
