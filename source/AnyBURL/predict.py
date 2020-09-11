# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file Apply.java
from logger import Logger
from utilities import current_milli_time
from data.triple_set import TripleSet
from config.config_yaml import Config
from rule_io.rule_reader import RuleReader
from structure.rule_engine import RuleEngine
from structure.rule import Rule

class Predict(object):

  def __init__(self, datasets='WN18'):
    self.cfg = Config.load_predict_config(datasets)
    self.datasets = datasets
    self.log = Logger.get_log_cate('prediction.txt', 'Predict')
    self.log.info('****************************start new section*************************************')
    self.log.info('initialize learning {}'.format(current_milli_time()))
    Rule.set_application_mode()

  def prediction(self, valid_set=False,extend=False):
    training_set, test_set, valid_set = TripleSet(), TripleSet(), TripleSet()
    training_set.read_triples(self.cfg['path_training'])
    test_set.read_triples(self.cfg['path_test'])
    valid_set.read_triples(self.cfg['path_valid'])

    path_rules_used = self.cfg['path_rules']
    #for path_rules_used in self.cfg['path_rules']:
    start_time = current_milli_time()
    tmp_path = path_rules_used.split('/')
    path_output_used = 'predictions/{}/{}'.format(self.datasets, tmp_path[2].replace('rule', 'predict'))
    self.log.info('rules learning: {}'.format(path_rules_used))
    self.log.info('output learning: {}'.format(path_output_used))
    rules = RuleReader(path_rules_used).read()
    if extend:
      rules_exd = RuleReader(self.cfg['path_rules_ext']).read()
      rules.extend(rules_exd)
      path_output_used = 'predictions/{}/ext_{}'.format(self.datasets, tmp_path[2].replace('rule', 'predict'))
      test_set, valid_set = valid_set, test_set
    elif valid_set:
      path_output_used = 'predictions/{}/predict_valid_1000.txt'.format(self.datasets)
      test_set, valid_set = valid_set, test_set

    rules_size = len(rules)
    print('*** read rules {} rom file {}'.format(rules_size, path_rules_used))
    rule_engine = RuleEngine(path_output_used, self.cfg['unseen_nagative_examples'])
    rule_engine.apply_rules_arx(rules, training_set, test_set, valid_set, self.cfg['top_k_output'])
    print('* evaluated {} rules to propose candiates for {} *2 completion tasks'.format(rules_size, len(test_set.triples)))
    print('* finished in {} ms.'.format(current_milli_time() - start_time))
    self.log.info('finished in {} s.'.format((current_milli_time() - start_time) // 1000))