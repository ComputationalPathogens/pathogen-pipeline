

process DOWNLOAD {
	input:
	  val(datadir)

	output:
	  val(datadir)

	script:
	"""
	ncbi-genome-download --formats fasta,assembly-report  --genera Brucella bacteria --parallel 4 -o "$datadir"
	"""
}