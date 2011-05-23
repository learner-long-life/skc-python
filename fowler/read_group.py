from skc.basic_approx.file import *
from skc.utils import *

# Read in enumerated, potential group members, and check for uniqueness
def read_and_simplify(l_0):
	sequences = []
	# Start numbering gates from 1, since identity is 0
	i = 1

	for generation_num in range(1,l_0+1):
		filename_pattern = filename_prefix + "-g" + str(generation_num) \
			+ "*.pickle"
		print str(filename_pattern)
		
		filenames = glob.glob(filename_pattern)
		if (len(filenames) == 0):
			raise RuntimeError("No files found for generation " + str(generation_num))
		for filename in filenames:
			new_sequences = read_from_file(filename)
			
			print "Generation " + str(generation_num) + ":"
			print str(len(new_sequences)) + " read"
			
			unique_sequences = []
	
			for new_op in new_sequences:
				print str(new_op)
				found = False
				for op in sequences:
					dist = fowler_distance(new_op.matrix, op.matrix)
					if (dist < TOLERANCE10):
						print "Non-unique sequence found: " + str(new_op) + " *** " + str(op)
						found = True
						break # This is the important part!
					#else:
					#	print "dist("+str(new_op)+","+str(op)+")=" + str(dist)
				
				# Update the sequences for the next iteration
				if (not found):
					new_op.name = "G" + str(i)
					i += 1
					sequences.append(new_op)

			print str(len(sequences))
	
	for sequence in sequences:
		print str(sequence)
	
	# Write out the final group to a file
	dump_to_file(sequences, "final-group-"+str(l_0))
