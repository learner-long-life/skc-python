from fowler.settings_su4 import *
from skc.basic_approx.file import filename_prefix
from skc.utils import *

sequences = []
# Start numbering gates from 1, since identity is 0
i = 1

for generation_num in [1,2,3]:
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
		
		if (generation_num == 1):
			unique_sequences = new_sequences
		else:
			unique_sequences = []

		for new_op in new_sequences:
			for op in sequences:
				if (fowler_distance(new_op.matrix, op.matrix) < TOLERANCE10):
					print "Non-unique sequence found: " + str(new_op) + " *** " + str(op)
				else:
					unique_sequences.append(new_op)
		sequences.extend(unique_sequences)
		print str(len(sequences))

for sequence in sequences:
	sequence.name = "G" + str(i)
	i += 1
	print str(sequence)
	