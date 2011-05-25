from fowler.btree import *
from skc.operator import *

key_list = ['H', 'X', 'Z', 'H']

btree_root = BNode()
btree_root.insert_data(key_list, I2)

print str(btree_root)

child1 = btree_root.get('H')

print str(child1)

child2 = child1.get('X')

print str(child2)

child3 = child2.get('Z')

print str(child3)
