
process TRAINXGB {
	echo true
	input:
	  val(k)
	  val(datapth)

	script:
	"""
	#!/usr/bin/env python
	import sys
	sys.path.append("$baseDir/pyfiles/")
	import trainmodel
	data,label_encoded_y, labels_unencoded = trainmodel.load_data("$datapth")
	final_models, final_features, final_labels = trainmodel.train_model($k, data, label_encoded_y, labels_unencoded, True, "$datapth")
	trainmodel.test_model(final_models, final_features, final_labels, labels_unencoded, "$datapth")
	"""
}