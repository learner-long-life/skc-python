import math
import numpy
import cPickle
import time

from skc.basic_approx import *

def generate_approxes(filename, iset, l0, simplify_rules):

	f = open(filename, 'wb')
	
	# Write the basic instruction set to a file
	cPickle.dump(iset, f, cPickle.HIGHEST_PROTOCOL)
	
	# Do it!
	basic_approxes = []

	# Start the generate timer
	begin_time = time.time()
	
	# Set the rules for simpifying later basic approxes
	init_simplify_engine(simplify_rules)
	
	# Collect all basic approxes for sequences of length 1 up to length l_0
	for i in range(l0):
		i_approxes = gen_basic_approx(iset, i+1)
		basic_approxes.extend(i_approxes)
		print "Number of basic approximations so far: " + str(len(basic_approxes))
	
	gen_time = time.time() - begin_time
	print "Generation time: " + str(gen_time)
	
	print "Writing basic approximations to file: " + filename
	
	begin_time = time.time()
	
	# Remove all the matrices to see if this saves us space
	# Yes, this saves us 85.3% (16M vs. 109M) for SU4
	for op in basic_approxes:
		del op.matrix
	
	# Write the approximations
	cPickle.dump(basic_approxes, f, cPickle.HIGHEST_PROTOCOL)
	
	write_time = time.time() - begin_time
	print "Writing time: " + str(write_time)
	
	print "Writing done, closing file."
	
	f.close()