#!/usr/bin/env nextflow

params.download = true
params.model = "xgb"
params.k = 5
params.ksize = 11
params.datadir = "$baseDir"

nextflow.enable.dsl = 2

include { METADATA } from './workflow/metadata'
include { FEATURES } from './workflow/features'
include { TRAIN } from './workflow/train'
include { DOWNLOAD } from './workflow/download'
include { TESTS } from './workflow/tests'
include { COLLECT } from './workflow/collect'

workflow {
	if(params.download == true) {
		DOWNLOAD(params.datadir)
		METADATA(params.k, DOWNLOAD.out)
	} else {
		METADATA(params.k, params.datadir)
	}
	nums = channel.from(29,31)
	COLLECT(METADATA.out, nums)
	COLLECT.out.done.view()
}

workflow.onComplete {
	log.info ( workflow.success ? "\nDone!" : "Oops .. something went wrong" )
}