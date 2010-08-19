import math
import numpy
import time

import skc.basic_approx

def generate_approxes(filename, iset, l0, simplify_rules):

	counter = 0

	skc.basic_approx.dump_to_file(iset, filename + "-iset")

	skc.basic_approx.filename_prefix = filename
	
	# Do it!
	basic_approxes = []

	# Start the generate timer
	begin_time = time.time()
	
	# Set the rules for simpifying later basic approxes
	skc.basic_approx.init_simplify_engine(simplify_rules)
	
	# Collect all basic approxes for sequences of length 1 up to length l_0
	for i in range(l0):
		i_approxes = skc.basic_approx.gen_basic_approx(iset, i+1)
		
		counter += len(i_approxes)
		basic_approxes.extend(i_approxes)
		
		# Do final chunking for this recursion level
		if (len(basic_approxes) >= skc.basic_approx.chunk_size):
			filename = filename_prefix + "-" + str(i)
			skc.basic_approx.dump_to_file(basic_approxes, filename)
			# Garbage collect the sequences
			basic_approxes = []

		print "Number of basic approximations so far: " + str(counter)
	
	gen_time = time.time() - begin_time
	print "Generation time: " + str(gen_time)
