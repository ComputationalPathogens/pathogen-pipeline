#!/usr/bin/env nextflow


process TRAINKERAS {
	echo true

	input:
	  val(k)
	  val(datapth)

	script:
	"""
	#!/usr/bin/env python
	import sys
	sys.path.append("$baseDir/pyfiles/")

	import trainmodel as tm

	data, label_encoded_y, labels_unencoded = tm.load_data("$datapth")
	final_hps, final_models, final_features, final_labels = tm.train_keras($k, data, label_encoded_y, labels_unencoded)
	tm.test_keras(final_models, final_features, final_labels)

	"""
}
