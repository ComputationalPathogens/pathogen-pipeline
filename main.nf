#!/usr/bin/env nextflow

params.download = true
params.features = true
params.start = 3
params.model = "xgb"
params.k = 5
params.datadir = "$baseDir"

nextflow.enable.dsl = 2

include { METADATA } from './workflow/metadata'
include { FEATURES } from './workflow/features'
include { TRAIN } from './workflow/train'
include { DOWNLOAD } from './workflow/download'

workflow {
	if(params.download == true) {
		DOWNLOAD(params.datadir)
		METADATA(params.k, DOWNLOAD.out)
	} else {
		METADATA(params.k, params.datadir)
	}
	if(params.features == true) {
		FEATURES(METADATA.out) 
		TRAIN(params.k, FEATURES.out, params.model)
	} else {
		TRAIN(params.k, METADATA.out, params.model)
	}
}

workflow.onComplete {
	log.info ( workflow.success ? "\nDone!" : "Oops .. something went wrong" )
}