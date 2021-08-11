params.datadir = "$baseDir"

include { KMERCOUNT } from './kmer'
include { BUILDMATRIX } from './buildmatrix'

workflow FEATURES {
	take:
	  datadir
	  ksize
	  
	main:
	  KMERCOUNT(datadir, ksize)
	  BUILDMATRIX(KMERCOUNT.out)

	emit:
	  BUILDMATRIX.out

}