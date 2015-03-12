import csv

with open('data/chr22_part.ERR001014.filt.bwa_aln.default.sam', 'rb') as f:
	r = csv.reader(f, delimiter='\t')
	qualities = []
	for read in r:
		qualities.append(read[4])

print len(filter(lambda x: int(x) > 30, qualities))
print len(filter(lambda x: int(x) == 0, qualities))
