
process SCATTERMAP {
    echo true
	input:
	  val(datadir)

	output:
	  stdout emit: filename

	script:
	"""
	#!python3
	import sys
	sys.path.append("$baseDir")
	from pyfiles import clustermap

	out = clustermap.create("$datadir")
	print(out, end = '')
	"""
}