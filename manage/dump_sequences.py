# Read sequences from a pickle file and print them out

from skc.basic_approx.file import *
import sys

if (len(sys.argv) < 2):
	print "Specify a pickle file to dump."
	sys.exit()

sequences = read_from_file(sys.argv[1])

for sequence in sequences:
	print str(sequence)
	