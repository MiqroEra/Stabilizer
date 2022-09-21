import numpy as np
import os

class treenode:
    def __init__(self, root=None, rootpos=None, 
                        i=None, x=None, y=None, z=None, 
                        value=None):
        self.root = root
        self.rootpos = rootpos
        self.i = i
        self.x = x
        self.y = y
        self.z = z
        self.value = value
    def no_branch(self):
        if self.i == None and self.x == None and self.y == None and self.z == None:
            return True
        else:
            return False  
    def go_back(self):
        if self.root is not None:
            return self.root
        else:
            raise Exception('This node has no root.')
    def mult(self, mp):
        if self.value is not None:
            self.value *= mp
        else:
            if self.i is not None:
                self.i.mult(mp)
            if self.x is not None:
                self.x.mult(mp)
            if self.y is not None:
                self.y.mult(mp)
            if self.z is not None:
                self.z.mult(mp)

class hf:
    def __init__(self, p):
        if type(p) == str:
            if os.path.exists(p):
                self.init_from_file(p)
            else:
                print('No such file! ---',p)
        else:
            self.init_qiskit(p)
        self.build_tree_from_op()
        self.states = ['?']*self.treedepth
        return
    def init_from_file(self, p):
        self.data = []
        self.operator = []
        self.tree = None
        with open(p, 'r') as f:
            for line in iter(f):
                if line == '':
                    break
                data, operator = line.split('*')
                if operator[-1] == '\n':
                    operator = operator[:-1]
                self.data.append(float(data))
                self.operator.append(operator)
    def init_qiskit(self, p):
        self.operator = p.primitive.paulis.to_labels()
        self.data = p.primitive.coeffs.real
        self.tree = None
    def print_the_node(self, node):
        line = ''
        while node.rootpos is not None:
            # print(node)
            line += node.rootpos
            node = node.root
        return line[::-1]
    def add_branch(self, node, thechar):
        if thechar == 'I':
            if node.i == None:
                node.i = treenode(root=node, rootpos='I')
            return node.i
        elif thechar == 'X':
            if node.x == None:
                node.x = treenode(root=node, rootpos='X')
            return node.x
        elif thechar == 'Y':
            if node.y == None:
                node.y = treenode(root=node, rootpos='Y')
            return node.y
        elif thechar == 'Z':
            if node.z == None:
                node.z = treenode(root=node, rootpos='Z')
            return node.z
        else:
            raise Exception('Undefined Symbol!',thechar)     
    def build_tree_from_op(self):
        self.tree = treenode()
        for i_idx, i in enumerate(self.operator):
            curnode = self.tree
            for j in i:
                curnode = self.add_branch(curnode, j)
            curnode.value = self.data[i_idx]
        self.energynode = self.get_node('I'*len(self.operator[0]))
        self.treedepth = len(self.operator[0])
        self.treetype = self.tree.__class__
        return
    def get_str_from_tree(self, curnode, s):
        if len(s) < self.treedepth:
            if curnode.i != None:
                self.get_str_from_tree(curnode.i, s+'I')
            if curnode.x != None:
                self.get_str_from_tree(curnode.x, s+'X')
            if curnode.y != None:
                self.get_str_from_tree(curnode.y, s+'Y')
            if curnode.z != None:
                self.get_str_from_tree(curnode.z, s+'Z')
        else:
            self.operator.append(s)
            self.data.append(curnode.value)
            return
        return
    def flush_operators(self):
        if type(self.tree) is None:
            raise Exception('There is no self.tree! Cannot generate operators.')
        self.operator = []
        self.data = []
        curnode = self.tree
        self.get_str_from_tree(curnode, '')
        return
    def get_noti(self, opr):
        notilist = []
        for j_idx, j in enumerate(opr):
            if j != 'I':
                notilist.append((j_idx, j))
        return notilist
    def is_term_exist(self, array):
        l = len(array)
        curnode = self.tree
        for i in range(l):
            thechar = array[i]
            if thechar == 'I':
                if curnode.i is not None:
                    curnode = curnode.i
                else:
                    i -= 1
                    break
            elif thechar == 'X':
                if curnode.x is not None:
                    curnode = curnode.x
                else:
                    i -= 1
                    break
            elif thechar == 'Y':
                if curnode.y is not None:
                    curnode = curnode.y
                else:
                    i -= 1
                    break
            elif thechar == 'Z':
                if curnode.z is not None:
                    curnode = curnode.z
                else:
                    i -= 1
                    break
            else:
                raise Exception('Illegal char!', thechar)
        if i == l-1:
            return True
        else:
            return False
    def get_node(self, array, check=True):
        if array == '':
            return self.tree
        if check and self.is_term_exist(array) is False:
            raise Exception('No such node!')
        curnode = self.tree
        for j in array:
            if j == 'I':
                curnode = curnode.i
            elif j == 'X':
                curnode = curnode.x
            elif j == 'Y':
                curnode = curnode.y
            elif j == 'Z':
                curnode = curnode.z
            else:
                raise Exception('Undefined Symbol!',j)
        return curnode
    def n_add_2n(self, n1, n2, mp):
        # here the node is surely exist
        # Deal with the I,X,Y,Z
        if n2.i is None and n1.i is not None:
            # Node -> None, 
            n1.i.root = n2 # change root (link n1.i to n2)
            # Don't need to care about rootpos, beacause it's I to I!
            n2.i = n1.i # copy n1.i (link n2 to n1.i)
            n2.i.mult(mp) # deal with the multiplier
        elif n1.i is not None:
            # node2.i not empty, node1.i not empty -> node to node!
            self.n_add_2n(n1.i, n2.i, mp)
        if n2.x is None and n1.x is not None:
            n1.x.root = n2
            n2.x = n1.x
            n2.x.mult(mp)
        elif n1.x is not None:
            self.n_add_2n(n1.x, n2.x, mp)
        if n2.y is None and n1.y is not None:
            n1.y.root = n2
            n2.y = n1.y
            n2.y.mult(mp)
        elif n1.y is not None:
            self.n_add_2n(n1.y, n2.y, mp)
        if n2.z is None and n1.z is not None:
            n1.z.root = n2
            n2.z = n1.z
            n2.z.mult(mp)
        elif n1.z is not None:
            self.n_add_2n(n1.z, n2.z, mp)
        # Deal with value
        if n1.value is not None:
            if n2.value is None:
                n2.value = n1.value * mp
            else:
                n2.value += n1.value * mp
        # Don't need to deal with rootpos
        return
    def fold_node_to_node(self, ngive, nget, mp, check=False):
        # ngive and nget are strings
        # check or create node 2
        if check:
            if self.is_term_exist(nget) is False: 
                curnode = self.tree
                for j in nget:
                    curnode = self.add_branch(curnode, j)
        node_give = self.get_node(ngive, check=False)
        node_get = self.get_node(nget, check=False)
        self.n_add_2n(node_give, node_get, mp)
        return
    def tree_set_qbit(self, qbit, tochar, mp):
        foldarray = []
        for i in self.operator:
            if i[qbit[0]] == qbit[1]:
                foldarray.append(i)
        for i in foldarray:
            if self.is_term_exist(i):
                print('Replace',i[:qbit[0]+1],'to',i[:qbit[0]]+tochar,',',qbit[1],'=',mp)
                self.fold_node_to_node(i[:qbit[0]+1], i[:qbit[0]]+tochar, mp, check=True)
                ngiveroot = self.get_node(i[:qbit[0]])
                # When one qbit is choose, such ad Z |phi> = -1 |phi>,
                # then X |phi> = 0 and the original data in tree 
                # need also be remove.
                chars = ['I', 'X', 'Y', 'Z']
                chars.remove(tochar)
                for j in chars:
                    if j == 'I':
                        ngiveroot.i = None
                    elif j == 'X':
                        ngiveroot.x = None
                    elif j == 'Y':
                        ngiveroot.y = None
                    elif j == 'Z':
                        ngiveroot.z = None
                    else:
                        raise Exception('No such symbol!', j)
        return
    def run(self):
        print('system energy:', self.data[0])
        while len(self.operator) >= 2:
            rank = np.argmax(np.abs(self.data[1:]))
            maxvalue =  self.data[1:][rank]
            maxopr = self.operator[1:][rank]
            print('The leading term:', maxopr, maxvalue)
            qbits = self.get_noti(maxopr)
            if len(qbits) > 1:
                l = len(self.operator)
                print()
                print('Can not deal with entangled state!(more than 2 q-bits)')
                print('Remaining', l,'terms')
                print('Now the states is:', *self.states)
                for i in range(l):
                    print('%15.8f\t%s' %(self.data[i],self.operator[i]))
                raise Exception('Finish running.')
            else:
                mp = 1 if self.get_node(maxopr).value < 0 else -1
                qbit = qbits[0]
                self.states[qbit[0]] = qbit[1]+'('+str(mp)+')'
                self.tree_set_qbit(qbits[0], 'I', mp)
                self.flush_operators()
                print('system energy:', self.data[0])
        return
    def get_state_energy(self, statestr):
        mps = []
        for i in statestr:
            k = 1 if i == '0' else -1
            mps.append(k)
        print('The basic energy:', self.data[0])
        for idx, i in enumerate(mps):
            qbit = (idx, 'Z')
            self.tree_set_qbit(qbit, 'I', i)
            self.flush_operators()
            print('system energy:', self.data[0])
