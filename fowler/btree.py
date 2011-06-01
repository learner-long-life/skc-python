# Btree data structure and methods for manipulating same to be find unique
# subsequences and their successors.

class BNode:

	# Canonical key order
	KEY_ORDER = []

	##########################################################################
	def __init__(self, key_in_parent=None):
		# Key in parent is used to find the next sibling. For root, it's None
		self.key_in_parent = key_in_parent
		self.children = {}
		
	##########################################################################
	# Returns true if we are a root (key_in_parent == None)
	def is_root(self):
		return (self.key_in_parent == None)
		
	##########################################################################
	# Returns true if we are a leaf (data exists in dir(self))
	def is_leaf(self):
		return ('data') in dir(self)
	
	##########################################################################
	# Peel off the next item of the key and pass the data on down recursively,
	# creating new children as we go, until we bottom out (len(key_list) == 0)
	# then insert the data into a leaf.
	# Make a defensive copy of the key_list, it will be modified!
	def insert_data(self, key_list, data):
		
		if (len(key_list) == 0):
			# If this is the base case, that's it: we're the leaf
			self.data = data
		else:
			# Peel off the key and add to the list
			next_key = key_list[0]

			key_list.remove(next_key)
			new_node = BNode(next_key)
			new_node.parent = self
			new_node.key_in_parent = next_key
			self.children[next_key] = new_node
			new_node.insert_data(key_list, data)
	
	##########################################################################
	# Find the data corresponding to the given key list, if it exists in tree
	# Return the node where the data is (if node.data != None)
	# or where the data would be (if node.data == None)
	# or None if the key is not found
	def find_data(self, key_list):

		if (len(key_list) == 0):
			# We are the leaf, and have been found!
			return self
			
		# Peel off the next item in the key
		next_key = key_list[0]
		next_child = None
		if (next_key in self.children.keys()):
			next_child = self.children[next_key]
			key_list.remove(next_key)
			# Recursively find the next child
			next_child = next_child.find_data(key_list)
			
		return next_child

	#########################################################################
	def __str__(self):
		if (self.key_in_parent != None):
			label = str(self.key_in_parent)
		else:
			label = "Root"
		string = label + ": " + str(self.children.keys()) + " "
		if ('data' in dir(self)):
			string += str(self.data)
		return string
		
	#########################################################################
	def get(self, key):
		return self.children[key]
	
	#########################################################################
	# Returns the next sibling to the child with the given key, if any exists
	# according to canonical key order.
	# Otherwise returns None
	def find_next_child(self, key):
		children_keys = self.children.keys()
		
		if ((key not in children_keys) or (key not in BNode.KEY_ORDER)):
			return None
			
		index1 = BNode.KEY_ORDER.index(key)
		
		# Initially set next_index to invalid value
		next_index = len(BNode.KEY_ORDER)
		for key2 in BNode.KEY_ORDER:
			if (key2 not in children_keys):
				continue
			index2 = BNode.KEY_ORDER.index(key2)
			if ((index2 > index1) and (index2 < next_index)):
				# Update the next index if we find one that's closer
				next_index = index2
		
		if (next_index != len(BNode.KEY_ORDER)):
			# If we've updated, then that means key2 must be in children_keys
			return self.children[BNode.KEY_ORDER[next_index]]
		else:
			return None
			
	##########################################################################
	# Find the leftmost child of the given node in the canonical KEY_ORDER
	# Return None otherwise
	def find_leftmost_child(self):
	
		for key in BNode.KEY_ORDER:
			if (key in self.children.keys()):
				return self.children[key]
		
		# Otherwise, there are no children, return None
		return None
	
	##########################################################################
	# Returns the successor in lexicographic order of the key list,
	# going as far back as the root
	def find_successor(self):
	
		current_node = self
		while (not current_node.is_root()):
			sibling = current_node.parent.find_next_child(current_node.key_in_parent)

			# Check if we have no sibling, if so, go up one more level
			if (sibling == None):
				current_node = current_node.parent
			else:
				break
		
		if (sibling == None):
			# If we can't find a next sibling, this is the lexicographically
			# last node
			return None
		else:
			# Else traverse the leftmost child of the sibling until we get to
			# leaf
			current_node = sibling
			while (not current_node.is_leaf()):
				current_node = current_node.find_leftmost_child()
			return current_node