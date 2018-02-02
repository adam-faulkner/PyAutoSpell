

import math

def normalize_by_column_L2_norm(feature_val):
	if feature_val == None:
		return
	if len(feature_val) == 0:
		return
	for j in range(len(feature_val)):
		column_sum = 0
		for i in range(len(feature_val)):
			column_sum +=feature_val[i] * feature_val[i]
			column_sum = math.sqrt(column_sum)
			for i in range(len(feature_val)):
				feature_val[i] /= column_sum
	return feature_val[i]


