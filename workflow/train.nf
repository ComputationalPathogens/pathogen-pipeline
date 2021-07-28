
include { TRAINXGB } from './trainxgb'
include { TRAINKERAS } from './trainkeras'

workflow TRAIN {
	take:
		k
		datapth
		model

	main:
		if(model == 'xgb') {
			TRAINXGB(k, datapth)
		} else {
			TRAINKERAS(k, datapth)
		}
}