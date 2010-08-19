from skc.operator import *
from skc.simplify import *

import types
import time
import cPickle

# Global variables
simplify_engine = None  # simplify engine
chunk_size = 1000000    # number of sequences to chunk together into a file
filename_prefix = ""    # prefix for pickled generated sequences

# Initialize the global simplify engine with the given rules for all
# subsequent generation of basic approximations
def init_simplify_engine(rules):
	global simplify_engine
	simplify_engine = SimplifyEngine(rules)

##############################################################################
def dump_to_file(object, filename):
	f = open(filename+".pickle", 'wb')
	
	begin_time = time.time()
	
	# Write the approximations
	cPickle.dump(object, f, cPickle.HIGHEST_PROTOCOL)
	
	write_time = time.time() - begin_time
	print "Writing time: " + str(write_time)
	
	print "Writing done, closing file."
	
	f.close()

##############################################################################
def chunk_sequences(sequences):
	# Do chunking if necessary
	if (len(sequences) >= chunk_size):
		filename = filename_prefix + prefix.ancestors_as_string()
		dump_sequences_to_file(prefix_sequences, filename)

##############################################################################
# Recursive helper method which enumerates all possible combinations of operators, given
# prefix - an array containing all operators so far concatenated (multiplied into a single matrix)
# iset - universal instruction set to use
# ops_left - integer >= 0 indicating the number of ops left to enumerate in each sequence.
# If ops_left = 1, this is the base case and we simply enumerate, using one op from iset 
# Returns - list of matrices consisting of enumerated sequences
def gen_basic_approx_helper(prefix, iset, ops_left):
	sequences = []
	total_length = 0
	sequence_count = 0
		
	if (ops_left <= 1):
		# Base case, enumerate over iset, appending one op to end of prefix each
		# We only need to simplify here
		#if (type(prefix) != types.NoneType):
		#	print "prefix= " + str(prefix.ancestors)
		for insn in iset:
			if (type(prefix) == types.NoneType):
				new_op = insn
			else:
				new_op = prefix.add_ancestors(insn)
			(simplify_length, new_sequence) = \
				simplify_engine.simplify(new_op.ancestors)
			# This is a hard-coded hack for now
			if (new_sequence == ['I']):
				continue
			#print str(new_sequence)
			#if (simplify_length > 0):
			#	print str(simplify_length) + " simplified"
			new_op.ancestors = new_sequence
			sequences.append(new_op)
			sequence_count += 1
			total_length += len(new_op.ancestors) 
	else:
		# Recursive case, generate sequences based on a particular choice of next instruction
		for insn in iset:
			if (type(prefix) == types.NoneType):
				new_prefix = insn
			else:
				new_prefix = prefix.add_ancestors(insn)
			(prefix_sequences, sequence_count, total_length_i) = \
				gen_basic_approx_helper(new_prefix, iset, ops_left-1)
			
			sequences.extend(prefix_sequences)
			sequence_len = len(sequences)
			sequence_count += sequence_len
			
			# Do chunking if necessary
			if (sequence_len >= chunk_size):
				chunk_prefix = sequences[sequence_len-1].ancestors_as_string()
				filename = filename_prefix + "-" + chunk_prefix
				dump_to_file(prefix_sequences, filename)
				# Garbage collect the sequences
				sequences = []				
				
			total_length += total_length_i
	
	return (sequences, sequence_count, total_length)

##############################################################################
## Generate table of basic approximations as preprocessing
# iset - array of dxd matrices, which correspond to operators of a universal instruction set
# l_0 - fixed length of sequences to generate for preprocessing table
def gen_basic_approx(iset, l_0):
	m = len(iset)
	print str(m) + " instructions found"
	
	first_op = iset[0] # Python uses 0-based indexing
	first_shape = first_op.matrix.shape
	
	if (len(first_shape) != 2):
		print "First operator is not a matrix! Shape = " +str(shape)
		return
	
	d = first_shape[0] # d=2 for qubits
	if (d != first_shape[1]):
		print "First operator is not a square matrix! Shape = " + str(shape)
		return
	
	for i in range(m):
		i_shape = iset[i].matrix.shape
		if (i_shape != first_shape):
			print "Operator " + str(i) + "'s shape does not match first shape: " + str(i_shape)
	
	file_counter = 0
	# Initial call to recursive helper method, with identity matrix as prefix
	(sequences, sequence_count, total_length) = gen_basic_approx_helper(None, iset, l_0)

	print str(sequence_count) + " sequences generated"
	print str(total_length) + " total length generated"

	return sequences

##############################################################################
# Find the closest basic approximation in approxes to arbitrary unitary u
# Based on operator norm distance
def find_basic_approx(approxes, u, distance):
	min_dist = numpy.finfo(numpy.float32).max # set to max float value at first
	closest_approx = None
	found = False
	for approx in approxes:
		#print "approx= " + str(approx)
		#print "u= " + str(u)
		current_dist = distance(approx.matrix,u.matrix)
		#print "current_dist= " + str(current_dist)
		#print "min_dist= " + str(min_dist)
		if (current_dist < min_dist):
			found = True
			min_dist = current_dist
			closest_approx = approx
			
	if (not found):
		raise RuntimeError("No closest approximation found.")
	
	return (closest_approx, min_dist)