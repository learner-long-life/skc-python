from fowler.btree import *
from skc.operator import *

key_list1 = ['H1', 'X1', 'Z2', 'H2']
key_list2 = ['S2d', 'Z1', 'X2', 'S1d']

BNode.KEY_ORDER = ['X1', 'X2', 'Z1', 'Z2', 'H1', 'H2', 'S1', 'S2', 'S1d', 'S2d',
	'CNOT12', 'CNOT21']

btree_root = BNode()

##############################################################################
# Insert the first key list and then trace it down the tree
print "*** INSERT FIRST KEY ***"

btree_root.insert_data(list(key_list1), I2)

print str(btree_root)

child1 = btree_root.get('H1')

print str(child1)

child2 = child1.get('X1')

print str(child2)

child3 = child2.get('Z2')

print str(child3)

child4 = child3.get('H2')

print str(child4)

##############################################################################
# Insert the second key list and then trace it down the tree
print "*** INSERT SECOND KEY ***"

btree_root.insert_data(list(key_list2), SZ)

print str(btree_root)

child1 = btree_root.get('S2d')

print str(child1)

child2 = child1.get('Z1')

print str(child2)

child3 = child2.get('X2')

print str(child3)

child4 = child3.get('S1d')

print str(child4)

##############################################################################
# Search for the next child at the top level
print "*** SEARCH FOR NEXT CHILD ***"

next_child = btree_root.find_next_child('H1')

print str(next_child)

##############################################################################
# Find first inserted node
print "*** FIND KEY 1 ***"

first_leaf = btree_root.find_data(key_list1)

print str(first_leaf)

##############################################################################
# Find second inserted node
print "*** FIND KEY 2 ***"

second_leaf = btree_root.find_data(key_list2)

print str(second_leaf)

##############################################################################
# Find leftmost child
print "*** FIND LEFTMOST CHILD ***"

left1 = btree_root.find_leftmost_child()

print str(left1)

left2 = child3.find_leftmost_child()

print str(left2)

##############################################################################
# Find successor
print "*** FIND SUCCESSOR ***"

successor = first_leaf.find_successor()

print str(successor)
