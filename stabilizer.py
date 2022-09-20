import sys
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

class stabilizer:
    def __init__(self, p):
        if type(p) == str:
            if os.path.exists(p):
                self.init_from_file(p)
            else:
                print('No such file! ---',p)
        else:
            self.init_qiskit(p)
        self.build_tree_from_op()
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
        self.treetype = self.tree.__class__
        return
    def get_str_from_tree(self, curnode, s, l):
        if len(s) < l:
            if curnode.i != None:
                self.get_str_from_tree(curnode.i, s+'I', l)
            if curnode.x != None:
                self.get_str_from_tree(curnode.x, s+'X', l)
            if curnode.y != None:
                self.get_str_from_tree(curnode.y, s+'Y', l)
            if curnode.z != None:
                self.get_str_from_tree(curnode.z, s+'Z', l)
        else:
            self.tmp_opr.append(s)
            self.tmp_data.append(curnode.value)
            return
        return
    def flush_operators(self):
        if type(self.tree) is None:
            raise Exception('There is no self.tree! Cannot generate operators.')
        self.operator = []
        self.data = []
        curnode = self.tree
        self.get_str_from_tree(curnode, '', len(self.operator[0]))
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
        if n2.i is None:
            if type(n1.i) == self.treetype:
                n1.i.root = n2
            n2.i = n1.i
        elif n1.i is not None:
            # node2.i not empty, node1.i not empty -> node to node!
            self.n_add_2n(n1.i, n2.i, mp)
        if n2.x is None:
            if type(n1.x) == self.treetype:
                n1.x.root = n2
            n2.x = n1.x
        elif n1.x is not None:
            self.n_add_2n(n1.x, n2.x, mp)
        if n2.y is None:
            if type(n1.y) == self.treetype:
                n1.y.root = n2
            n2.y = n1.y
        elif n1.y is not None:
            self.n_add_2n(n1.y, n2.y, mp)
        if n2.z is None:
            if type(n1.z) == self.treetype:
                n1.z.root = n2
            n2.z = n1.z
        elif n1.z is not None:
            self.n_add_2n(n1.z, n2.z, mp)
        if n1.value is not None:
            if n2.value is None:
                n2.value = n1.value * mp
            else:
                n2.value += n1.value * mp
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
    def treefold(self, qbit, tochar, mp):
        foldarray = []
        for i in self.operator:
            if i[qbit[0]] == qbit[1]:
                foldarray.append(i)
        for i in foldarray:
            if self.is_term_exist(i):
                print('Now change',i[:qbit[0]+1],'to',i[:qbit[0]]+tochar)
                print('Choose',qbit[1],'to be',mp)
                self.fold_node_to_node(i[:qbit[0]+1], i[:qbit[0]]+tochar, mp, check=True)
                ngiveroot = self.get_node(i[:qbit[0]]) 
                if qbit[1] == 'I':
                    ngiveroot.i = None
                elif qbit[1] == 'X':
                    ngiveroot.x = None
                elif qbit[1] == 'Y':
                    ngiveroot.y = None
                elif qbit[1] == 'Z':
                    ngiveroot.z = None
                else:
                    raise Exception('No such symbol!', qbit[1])
        return
    def run(self):
        self.operator, self.data = self.flush_operators()
        print('system energy:', self.data[0])
        while len(self.operator) > 2:
            rank = np.argmax(np.abs(self.data[1:]))
            maxvalue =  self.data[1:][rank]
            maxopr = self.operator[1:][rank]
            qbits = self.get_noti(maxopr)
            if len(qbits) > 1:
                l = len(self.operator)
                print()
                print('Can not deal with entangled state!(more than 2 q-bits)')
                print('Remaining', l,'terms')
                for i in range(l):
                    print('%15.8f\t%s' %(self.data[i],self.operator[i]))
                raise Exception('Finish running.')
            else:
                print('The leading term:', maxopr, maxvalue)
                mp = 1 if self.get_node(maxopr).value < 0 else -1
                self.treefold(qbits[0], 'I', mp)
                self.operator, self.data = self.flush_operators()
                print('system energy:', self.data[0])
        return
