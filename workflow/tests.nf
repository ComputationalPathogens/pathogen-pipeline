
process TESTS {
	echo true
	input:
	  val(datadir)

	output:
	  stdout emit: out


	script:
	"""
    pytest $datadir
	"""
}