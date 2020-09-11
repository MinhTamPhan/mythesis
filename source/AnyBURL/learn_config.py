class ConfigParameters(object):
  '''/**
	* Number of maximal attempts to create body grounding. Every partial body grounding is counted.
	*/'''
  trial_size = 1000000

  '''/**
	* Used for restricting the number of samples drawn for computing scores as confidence.
	*/'''
  sample_size = 1000
  '''/**
	 * The time that is reserved for one batch in milliseconds. Each second batch is
	 * used for mining cyclic/acyclic rules.
	 */'''
  batch_time = 10
  '''/**
	 * The threshold for the number of correctly prediction within the given training set.
	 */'''
  threshold_correct_predictions = 5

  '''/**
	 * The threshold for the confidences.
	 */'''
  threshold_confidence = 0.05
  '''/**
	 * The saturation required to move to the next rule length. Saturation is defined as the fraction of
	 * useful rules that have been sampled in a previous batch compared to all useful rules that have
	 * been sampled within that batch. If the saturation is above the value, longer rules are sampled.
	 */'''
  saturation = 0.675
  '''/**
	 * The maximal number of body atoms in cyclic rules (inclusive this number). If this number is exceeded all computation time
	 * is used for acyclic rules only from that time on.
	 *
	 */'''
  max_length_cylic = 2