
process PROCESSFILES {
	echo true
	input:
	  val(datadir)

	output:
	  stdout emit: out


	script:
	"""
	#!/usr/bin/env python
	import sys
	import os
	sys.path.append("$baseDir/pyfiles/")
	import metadata

	out = metadata.build_metadata("$datadir")
	print(out, end = '')
	"""
}