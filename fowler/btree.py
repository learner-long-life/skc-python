# Btree data structure and methods for manipulating same to be find unique
# subsequences and their successors.

class BNode:

	def __init__(self):
		self.keys = set([])
		self.children = {}
	
	# Peel off the next item of the key and pass the data on down recursively,
	# creating new children as we go, until we bottom out
	# then insert the data into a leaf.
	def insert_data(self, key_list, data):
		if (len(key_list) < 1):
			raise RuntimeError("Cannot have zero-length key")
		
		# Peel off the key and add to the list
		next_key = key_list[0]
		self.keys.add(next_key)
		
		if (len(key_list) == 1):
			# If this is the base case, that's it: we're the leaf
			self.data = data
		else:
			# Peel off the next item in the key
			key_list.remove(next_key)
			new_node = BNode()
			new_node.parent = self
			self.children[next_key] = new_node
			new_node.insert_data(key_list, data)
	
	# Find the data corresponding to the given key list, if it exists in tree
	# Return the node where the data is (if node.data != None)
	# or where the data would be (if node.data == None)
	# or None if the key is not found
	def find_data(self, key_list):
		if (len(key_list) < 1):
			raise RuntimeError("Cannot have zero-length key")

		next_key = key_list[0]
		next_child = None
		if (next_key in self.children.keys()):
			next_child = self.children[next_key]
			
		if (len(key_list) > 1):
			# Peel off the next item in the key
			key_list.remove(next_key)
			# Recursively find the next child
			next_child = next_child.find_data(key_list)
			
		return next_child

	def __str__(self):
		string = str(self.keys) + ": "
		if ('data' in dir(self)):
			string += str(self.data)
		return string
		
	def get(self, key):
		return self.children[key]