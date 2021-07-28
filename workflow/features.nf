params.datadir = "$baseDir"

include { KMERCOUNT } from './kmer'
include { BUILDMATRIX } from './buildmatrix'

workflow FEATURES {
	take:
	  datadir

	main:
	  KMERCOUNT(datadir)
	  BUILDMATRIX(KMERCOUNT.out)

	emit:
	  BUILDMATRIX.out

}