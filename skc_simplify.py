class SimplifyEngine:

	#-------------------------------------------------------------------------
	def __init__(self, rules):
		self.rules = rules
		self.min_arg_count = 255 # This is a pretty safe heuristic
		for rule in self.rules:
			if (rule.arg_count < self.min_arg_count):
				self.min_arg_count = rule.arg_count
	
	#-------------------------------------------------------------------------
	# If sequence is non-empty at beginning of method,
	# transfer one element from sequence to scratch and returns True
	# otherwise returns False
	def transfer_to_scratch(self, sequence, scratch):
		if (len(sequence) > 0):
			new_op = sequence.pop(len(sequence)-1)
			scratch.insert(0, new_op)
			return True
		else:
			return False
		#print "transfer_to_scratch= " + str(scratch)
				
	#-------------------------------------------------------------------------
	# Fill the scratch sequence up to the arg_count of any rule
	def fill_scratch_sequence(self, sequence, scratch):
		long_enough = True
		while (long_enough and (len(scratch) < self.min_arg_count)):
			long_enough = self.transfer_to_scratch(sequence, scratch)
		if (long_enough):
			assert(len(scratch) >= self.min_arg_count)

	#-------------------------------------------------------------------------
	# The main simplify method called from outside				
	def simplify(self, sequence):
		# Get the length of the old sequence for comparison below
		simplify_length = len(sequence)

		# Make a defensive copy
		sequence = list(sequence)
		scratch_sequence = []
		 # This is reset in every iteration below, just declare it here so
		 # we have access to it in the first While test (kludge!)
		global_obtains = False
		global_any_obtains = False
		
		while ((len(sequence) > 0) or global_obtains):
			global_obtains = False
			#print "Entering while loop!"
		
			# Prefill the scratch space to min_arg_count
			self.fill_scratch_sequence(sequence, scratch_sequence)
		
			# Apply the rules repeatedly in scratch_space until none of them
			# obtain
			first = True
			any_obtains = False
			while (first or any_obtains):
				any_obtains = False
				first = False
				for rule in (self.rules):
					obtains = False
					first_time = True
					# If we don't obtain or have enough arguments for this
					# rule, skip it
					while ((first_time or obtains) and
					       (len(scratch_sequence) >= rule.arg_count)):
						first_time = False
						# Set the outer condition to repeat all rules later
						# Repeat this rule now, in case it obtains again
						obtains = rule.simplify(scratch_sequence)
						if (obtains):
							any_obtains = True
							global_obtains = True
							global_any_obtains = True
			#print "global_obtains= " + str(global_obtains)
						
			# Now the scratch sequence is stale, so let's get a fresh op
			self.transfer_to_scratch(sequence, scratch_sequence)
			#print str(global_obtains)
			#print str(scratch_sequence)
			#print str(sequence)
			
		simplify_length -= len(scratch_sequence)
			
		# The old sequence should be empty, return the scratch
		return (simplify_length, scratch_sequence)
					
##############################################################################
class SimplifyRule:

	def __init__(self, slogan, arg_count):
		self.slogan = slogan
		self.arg_count = arg_count
		
	def __str__(self):
		return self.slogan + "(" + str(self.arg_count) + ")"
		
	def simplify(self, arg_list):
		# Delegate to subclass-specific implementation
		(obtains, C) = self.__simplify__(arg_list)
		# Intercept here before returning, and pop the simplified arguments
		# off the list
		if (obtains):
			#print str(self) + " OBTAINS!"
			for i in range(self.arg_count):
				arg_list.pop(0)
			arg_list.insert(0, C)
			#print str(arg_list)
		return obtains
		
##############################################################################
class AdjointRule(SimplifyRule):

	def __init__(self):
		SimplifyRule.__init__(self, "Q*Q\dagger = I", 2)
		
	def __simplify__(self, arg_list):
		# This rule starts out not obtaining by default
		activated = False
		C = ''
		
		# Get the first character of the first two arguments
		A = arg_list[0]
		B = arg_list[1]
		len_A1 = len(A)-1
		len_B1 = len(B)-1
		An = A[len_A1]
		Bn = B[len_B1]
		# All of A except last character
		A0n1 = A[0:len_A1]
		# All of B except last character
		B0n1 = B[0:len_B1]
		if ((A == B0n1) and (Bn == 'd')):
			# Test if B is the adjoint of A
			C = 'I'
			#print "A= " + str(A)
			#print "B0n1= " + str(B0n1)
			#print "Bn= " + str(Bn)
			activated = True
		elif ((B == A0n1) and (An == 'd')):
			# Test if A is the adjoint of B
			C = 'I'
			activated = True
			
		return (activated, C) 
		
##############################################################################
class DoubleIdentityRule(SimplifyRule):
	def __init__(self, symbol):
		self.symbol = symbol
		SimplifyRule.__init__(self, "Q*Q = I", 2)
		
	def __simplify__(self, arg_list):
		activated = False
		A = arg_list[0]
		B = arg_list[1]
		C = ''
		if ((A==self.symbol) and (B==self.symbol)):
			activated = True
			C = 'I'
			
		return (activated, C)

##############################################################################
class IdentityRule(SimplifyRule):
	def __init__(self):
		SimplifyRule.__init__(self, "I*Q = Q", 2)
		
	def __simplify__(self, arg_list):
		activated = False
		A = arg_list[0]
		B = arg_list[1]
		C = ''
		if (A=='I'):
			activated = True
			C = B
		elif (B=='I'):
			activated = True
			C = A

		return (activated, C)
	