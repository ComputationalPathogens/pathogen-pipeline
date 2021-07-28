
process KMERCOUNT {
	echo true
	input:
	  val(datadir)

	output:
	  stdout emit: dumpname

	script:
	"""
	#!/usr/bin/env python
	import sys
	sys.path.append("$baseDir/pyfiles/")
	import kmer

	out = kmer.count_kmer("$datadir")
	print(out, end = '')
	"""
}