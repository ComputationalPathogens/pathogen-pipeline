#!/usr/bin/env nextflow
params.download = true
params.k = 5
params.datadir = "$baseDir"
params.genera = "Bacillus anthracis"

nextflow.enable.dsl = 2

include { METADATA } from './workflow/metadata'
include { FEATURES } from './workflow/features'
include { DOWNLOAD } from './workflow/download'
include { SCATTERMAP } from './workflow/graphs'
workflow {
	if(params.download == true) {
		DOWNLOAD(params.datadir, params.genera)
		METADATA(params.k, DOWNLOAD.out)
	} else {
		METADATA(params.k, params.datadir)
	}
	FEATURES(METADATA.out, ksize)
    SCATTERMAP(FEATURES.out)
}

workflow.onComplete {
	log.info ( workflow.success ? "\nDone!" : "Oops .. something went wrong" )
}