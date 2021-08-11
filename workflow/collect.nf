include { KFREQ } from './kfreq'

workflow COLLECT {
	take:
	  datadir
	  ksize
	  
	main:
	  KFREQ(datadir, ksize)

	emit:
	  done = KFREQ.out.cntname

}