# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file Config.java

import yaml

class Config(object):

  def __init__(self):
    pass

  def load_eval_config(dataset='WN18'):
    with open('config/eval_config.yaml') as stream:
    # use safe_load instead load
      config_yaml = yaml.safe_load(stream)
      if dataset == 'WN18':
        config_yaml['path_prediction'] = config_yaml['path_prediction'][2]
        config_yaml['path_training'] = config_yaml['path_training'][2]
        config_yaml['path_valid'] = config_yaml['path_valid'][2]
        config_yaml['path_test'] = config_yaml['path_test'][2]
        config_yaml['path_prediction_ext'] = config_yaml['path_prediction_ext'][2]
        config_yaml['path_eval_predict'] = config_yaml['path_eval_predict'][2]
      elif dataset == 'FB15k':
        config_yaml['path_prediction'] = config_yaml['path_prediction'][0]
        config_yaml['path_training'] = config_yaml['path_training'][0]
        config_yaml['path_valid'] = config_yaml['path_valid'][0]
        config_yaml['path_test'] = config_yaml['path_test'][0]
        config_yaml['path_prediction_ext'] = config_yaml['path_prediction_ext'][0]
        config_yaml['path_eval_predict'] = config_yaml['path_eval_predict'][0]
      elif dataset == 'FB15k-237':
        config_yaml['path_prediction'] = config_yaml['path_prediction'][1]
        config_yaml['path_training'] = config_yaml['path_training'][1]
        config_yaml['path_valid'] = config_yaml['path_valid'][1]
        config_yaml['path_test'] = config_yaml['path_test'][1]
        config_yaml['path_prediction_ext'] = config_yaml['path_prediction_ext'][1]
        config_yaml['path_eval_predict'] = config_yaml['path_eval_predict'][1]
      elif dataset == 'WN18RR':
        config_yaml['path_prediction'] = config_yaml['path_prediction'][3]
        config_yaml['path_training'] = config_yaml['path_training'][3]
        config_yaml['path_valid'] = config_yaml['path_valid'][3]
        config_yaml['path_test'] = config_yaml['path_test'][3]
        config_yaml['path_prediction_ext'] = config_yaml['path_prediction_ext'][3]
        config_yaml['path_eval_predict'] = config_yaml['path_eval_predict'][3]
      config_yaml['dataset'] = dataset
      return config_yaml

  def load_learning_config(dataset='WN18'):
    with open('config/learning_config.yaml') as stream:
    # use safe_load instead load
      config_yaml = yaml.safe_load(stream)
      if dataset == 'WN18':
        config_yaml['path_training'] = config_yaml['path_training'][2]
      elif dataset == 'FB15k':
        config_yaml['path_training'] = config_yaml['path_training'][0]
      elif dataset == 'FB15k-237':
        config_yaml['path_training'] = config_yaml['path_training'][1]
      elif dataset == 'WN18RR':
        config_yaml['path_training'] = config_yaml['path_training'][3]
      config_yaml['dataset'] = dataset
      return config_yaml

  def load_predict_config(dataset='WN18'):
    # path_rules, path_training, path_valid, path_test
    with open('config/predict_config.yaml') as stream:
    # use safe_load instead load
      config_yaml = yaml.safe_load(stream)
      if dataset == 'WN18':
        config_yaml['path_rules'] = config_yaml['path_rules'][2]
        config_yaml['path_training'] = config_yaml['path_training'][2]
        config_yaml['path_valid'] = config_yaml['path_valid'][2]
        config_yaml['path_test'] = config_yaml['path_test'][2]
        config_yaml['path_rules_ext'] = config_yaml['path_rules_ext'][2]
      elif dataset == 'FB15k':
        config_yaml['path_rules'] = config_yaml['path_rules'][0]
        config_yaml['path_training'] = config_yaml['path_training'][0]
        config_yaml['path_valid'] = config_yaml['path_valid'][0]
        config_yaml['path_test'] = config_yaml['path_test'][0]
        config_yaml['path_rules_ext'] = config_yaml['path_rules_ext'][0]
      elif dataset == 'FB15k-237':
        config_yaml['path_rules'] = config_yaml['path_rules'][1]
        config_yaml['path_training'] = config_yaml['path_training'][1]
        config_yaml['path_valid'] = config_yaml['path_valid'][1]
        config_yaml['path_test'] = config_yaml['path_test'][1]
        config_yaml['path_rules_ext'] = config_yaml['path_rules_ext'][1]
      elif dataset == 'WN18RR':
        config_yaml['path_rules'] = config_yaml['path_rules'][3]
        config_yaml['path_training'] = config_yaml['path_training'][3]
        config_yaml['path_valid'] = config_yaml['path_valid'][3]
        config_yaml['path_test'] = config_yaml['path_test'][3]
        config_yaml['path_rules_ext'] = config_yaml['path_rules_ext'][3]
      config_yaml['dataset'] = dataset
      return config_yaml