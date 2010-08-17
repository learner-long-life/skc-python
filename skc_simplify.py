class SimplifyRule:

	def __init__(self, slogan, arg_count):
		self.slogan = slogan
		self.arg_count = arg_count
		
	def __str__(self):
		return self.slogan + "(" + str(arg_count) + ")"

##############################################################################
class AdjointRule(SimplifyRule):

	def __init__(self):
		SimplifyRule.__init__(self, "Q*Q\dagger = I", 2)
		
	def simplify(self, arg_list):
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
			print "A= " + str(A)
			print "B0n1= " + str(B0n1)
			print "Bn= " + str(Bn)
			activated = True
		elif ((B == A0n1) and (An == 'd')):
			# Test if A is the adjoint of B
			C = 'I'
			activated = True
			
		return (activated, C) 
		
##############################################################################
class DoubleIdentityRule(SimplifyRule):
	def __init__(self):
		SimplifyRule(self, "I*I = I", 2)
		
	def simplify(arg_list):
		activated = False
		if ((A=='I') and (B=='I')):
			activated = True
			C = 'I'
			
		return (activated, C)
	