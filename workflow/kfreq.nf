
process KFREQ {
    echo true
	input:
	  val(datadir)
	  val(ksize)

	output:
	  stdout emit: cntname

	script:
	"""
	#!python3
	import sys
	sys.path.append("$baseDir")
	from pyfiles import kfreq

	out = kfreq.genome_freqs("$datadir", $ksize)
	print(out, end = '')
	"""
}