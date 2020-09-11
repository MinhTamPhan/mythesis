# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file Learn.java
from algorithm.path_sampler import PathSampler
from structure.rule import Rule
from data.triple_set import TripleSet
from learn_config import ConfigParameters
from logger import Logger
from utilities import current_milli_time
from config.config_yaml import Config
import time
import copy
import threading
from os import remove, path
import os


class Learning(object):

  def __init__(self, dataset='WN18'):
    self.log = Logger.get_log_cate('learning.txt', 'Learning')
    self.cfg = Config.load_learning_config(dataset)
    self.log.info('****************************start new section*************************************')
    self.log.info('initialize learning {}'.format(current_milli_time()))
    self.triple_set = TripleSet()
    self.triple_set.read_triples(self.cfg['path_training'])

  def train(self):
    triple_set = self.triple_set
    index_start_time = current_milli_time()
    self.log.info('training with config {}'.format(self.cfg))
    path_sampler = PathSampler(triple_set)
    path_counter, batch_counter = 0, 0
    mine_cyclic_not_acyclic = False
    all_useful_rules = [set()]
    snapshot_index, rule_size_cyclic, rule_size_acyclic = 0, 0, 0
    last_cyclic_coverage, last_acyclic_coverage = 0.0,0.0
    self.log.info('indexing dataset: {}'.format(self.cfg['path_training']))
    self.log.info('time elapsed: {} ms'.format(current_milli_time() - index_start_time))
    snapshots_at = self.cfg['snapshots_at']
    dataset = self.cfg['dataset']
    start_time = current_milli_time()
    while True:
      batch_previously_found_rules, batch_new_useful_rules, batch_rules = 0, 0, 0
      rule_size = rule_size_cyclic if mine_cyclic_not_acyclic else rule_size_acyclic
      useful_rules = all_useful_rules[rule_size]
      elapsed_seconds = (current_milli_time() - start_time) // 1000
      ## snapshots rule affter t seconds white learning
      if elapsed_seconds > snapshots_at[snapshot_index]:
        total_rule = 0
        for _rules in all_useful_rules:
          total_rule += len(_rules)
        snapshot_file = 'learning_rules/{}/rule_{}.txt'.format(dataset, snapshots_at[snapshot_index])
        snapshot_index += 1
        self.log.info('snapshot_rules: {} in file {}'.format(total_rule, snapshot_file))
        snapshot_rules = copy.deepcopy(all_useful_rules)
        thread_snapshot = threading.Thread(target=self.process_snapshot_rule, args=(snapshot_rules, snapshot_file, ))
        thread_snapshot.start()
        print('created snapshot {} after {} seconds'.format(snapshot_index, elapsed_seconds))
        if snapshot_index == len(snapshots_at):
          print('*************************done learning*********************************')
          thread_snapshot.join()
          return 0
      # batch learnig
      batch_start_time = current_milli_time()
      while True:
        if current_milli_time() - batch_start_time > self.cfg['batch_time']:
          break
        path_counter += 1
        path = path_sampler.sample_path(rule_size + 2, mine_cyclic_not_acyclic)
        if path != None and path.is_valid():
          rule = Rule()
          rule.init_from_path(path)
          gen_rules = rule.get_generalizations(mine_cyclic_not_acyclic)
          for r in gen_rules:
            if r.is_trivial():
              continue
            batch_rules += 1
            if r not in useful_rules:
              r.compute_scores(triple_set)
            if r.confidence >= self.cfg['threshold_confidence'] and r.correctly_predicted >= self.cfg['threshold_correct_predictions']:
              batch_new_useful_rules += 1
              useful_rules.add(r)
            else:
              batch_previously_found_rules += 1

      batch_counter += 1
      str_type = 'CYCLIC' if mine_cyclic_not_acyclic else 'ACYCLIC'
      print('=====> batch [{} {}] {} (sampled {} pathes) *****'.format(str_type, rule_size + 1, batch_counter, path_counter))
      current_coverage = batch_previously_found_rules / (batch_new_useful_rules + batch_previously_found_rules)
      print('=====> fraction of previously seen rules within useful rules in this batch: {} num of new rule = {} num of previously rule = {} num of all batch rules = {}'.format(current_coverage,batch_new_useful_rules, batch_previously_found_rules, batch_rules))
      print('=====> stored rules: {}'.format(len(useful_rules)))
      if mine_cyclic_not_acyclic:
        last_cyclic_coverage = current_coverage
      else:
        last_cyclic_coverage = current_coverage

      if current_coverage > self.cfg['saturation'] and batch_previously_found_rules > 1:
        rule_size += 1
        if mine_cyclic_not_acyclic:
          rule_size_cyclic = rule_size
        if not mine_cyclic_not_acyclic:
          rule_size_acyclic = rule_size
        print('=========================================================')
        print('=====> increasing rule size of {} rule to {}'.format(str_type, rule_size + 1))
        self.log.info('increasing rule size of {} rules to {}  after {} s'.format(str_type, rule_size + 1, (current_milli_time() - start_time)//1000))
        all_useful_rules.append(set())

      mine_cyclic_not_acyclic = not mine_cyclic_not_acyclic
      if mine_cyclic_not_acyclic and rule_size_cyclic + 1 > self.cfg['max_length_cylic']:
        mine_cyclic_not_acyclic = False

  def process_snapshot_rule(self, rules, file):
    if path.exists(file):
      remove(file)
    with open(file, 'w') as output_stream:
      for set_rule in rules:
        for rule in set_rule:
          print(rule, file=output_stream)

  def process_snapshot_rule_exis_file(self, rules, file):
    with open(file, 'a+') as output_stream:
      for set_rule in rules:
        for rule in set_rule:
          print(rule, file=output_stream)

  def train_with_batch(self, batch_triple, batch_time=100):
    is_connected, new_triple = self.triple_set.add_batch_triple(batch_triple)
    if is_connected:
      triple_set =  self.triple_set
      path_sampler = PathSampler(triple_set)
      index_start_time = current_milli_time()
      self.log.info('train_with_batch triple_set: {}, new_triple: {}'.format(len(triple_set.triples), len(new_triple.triples)))
      path_counter, batch_counter = 0, 0
      mine_cyclic_not_acyclic = False
      all_useful_rules = [set()]
      snapshot_index, rule_size_cyclic, rule_size_acyclic = 0, 0, 0
      last_cyclic_coverage, last_acyclic_coverage = 0.0,0.0
      self.log.info('indexing dataset: {}'.format(self.cfg['path_training']))
      self.log.info('time elapsed: {} ms'.format(current_milli_time() - index_start_time))
      dataset = self.cfg['dataset']
      start_time = current_milli_time()
      while True:
        batch_previously_found_rules, batch_new_useful_rules, batch_rules = 0, 0, 0
        rule_size = rule_size_cyclic if mine_cyclic_not_acyclic else rule_size_acyclic
        useful_rules = all_useful_rules[rule_size]
        elapsed_seconds = (current_milli_time() - start_time) // 1000
        if elapsed_seconds > batch_time:
          total_rule = 0
          for _rules in all_useful_rules:
            total_rule += len(_rules)
          snapshot_file = 'learning_rules/{}/rule_extend_{}.txt'.format(dataset, 800)
          self.log.info('***************************************************************')
          self.log.info('**snapshot_rules: {} in file {}'.format(total_rule, snapshot_file))
          self.log.info('***************************************************************')
          snapshot_rules = copy.deepcopy(all_useful_rules)
          thread_snapshot = threading.Thread(target=self.process_snapshot_rule, args=(snapshot_rules, snapshot_file, ))
          thread_snapshot.start()
          print('created snapshot {} after {} seconds'.format(total_rule, elapsed_seconds))
          print('*************************done learning*********************************')
          thread_snapshot.join()
          return 0
        batch_start_time = current_milli_time()
        while True:
          if current_milli_time() - batch_start_time > self.cfg['batch_time']:
            break
          path_counter += 1
          path = path_sampler.sample_batch_path(rule_size + 2, new_triple, mine_cyclic_not_acyclic)
          if path != None and path.is_valid():
            rule = Rule()
            rule.init_from_path(path)
            gen_rules = rule.get_generalizations(mine_cyclic_not_acyclic)
            for r in gen_rules:
              if r.is_trivial():
                continue
              batch_rules += 1
              if r not in useful_rules:
                r.compute_scores(triple_set)
              if r.confidence >= self.cfg['threshold_confidence'] and r.correctly_predicted >= self.cfg['threshold_correct_predictions']:
                batch_new_useful_rules += 1
                useful_rules.add(r)
              else:
                batch_previously_found_rules += 1
        batch_counter += 1
        str_type = 'CYCLIC' if mine_cyclic_not_acyclic else 'ACYCLIC'
        print('=====> batch [{} {}] {} (sampled {} pathes) *****'.format(str_type, rule_size + 1, batch_counter, path_counter))
        current_coverage = batch_previously_found_rules / (batch_new_useful_rules + batch_previously_found_rules)
        print('=====> fraction of previously seen rules within useful rules in this batch: {} num of new rule = {} num of previously rule = {} num of all batch rules = {}'.format(current_coverage,batch_new_useful_rules, batch_previously_found_rules, batch_rules))
        print('=====> stored rules: {}'.format(len(useful_rules)))
        if mine_cyclic_not_acyclic:
          last_cyclic_coverage = current_coverage
        else:
          last_cyclic_coverage = current_coverage

        if current_coverage > self.cfg['saturation'] and batch_previously_found_rules > 1:
          rule_size += 1
          if mine_cyclic_not_acyclic:
            rule_size_cyclic = rule_size
          if not mine_cyclic_not_acyclic:
            rule_size_acyclic = rule_size
          print('=========================================================')
          print('=====> increasing rule size of {} rule to {}'.format(str_type, rule_size + 1))
          self.log.info('increasing rule size of {} rules to {}  after {} s'.format(str_type, rule_size + 1, (current_milli_time() - start_time)//1000))
          all_useful_rules.append(set())

        mine_cyclic_not_acyclic = not mine_cyclic_not_acyclic
        if mine_cyclic_not_acyclic and rule_size_cyclic + 1 > self.cfg['max_length_cylic']:
          mine_cyclic_not_acyclic = False

  def train_with_edge(self, triple):
    is_connected, new_triple = self.triple_set.add_edge_triple(triple)
    if is_connected:
      triple_set =  self.triple_set
      path_sampler = PathSampler(triple_set)
      index_start_time = current_milli_time()
      self.log.info('train_with_batch triple_set: {}, new_triple: {}'.format(len(triple_set.triples), new_triple))
      path_counter, batch_counter = 0, 0
      mine_cyclic_not_acyclic = False
      all_useful_rules = [set()]
      snapshot_index, rule_size_cyclic, rule_size_acyclic = 0, 0, 0
      last_cyclic_coverage, last_acyclic_coverage = 0.0,0.0
      self.log.info('indexing dataset: {}'.format(self.cfg['path_training']))
      self.log.info('time elapsed: {} ms'.format(current_milli_time() - index_start_time))
      dataset = self.cfg['dataset']
      start_time = current_milli_time()
      while True:
        batch_previously_found_rules, batch_new_useful_rules, batch_rules = 0, 0, 0
        rule_size = rule_size_cyclic if mine_cyclic_not_acyclic else rule_size_acyclic
        useful_rules = all_useful_rules[rule_size]
        elapsed_seconds = (current_milli_time() - start_time) // 1000
        if elapsed_seconds > 1:
          total_rule = 0
          for _rules in all_useful_rules:
            total_rule += len(_rules)
          snapshot_file = 'learning_rules/{}/rule_extend_{}.txt'.format(dataset, 20)
          self.log.info('***************************************************************')
          self.log.info('**snapshot_rules: {} in file {}'.format(total_rule, snapshot_file))
          self.log.info('***************************************************************')
          snapshot_rules = copy.deepcopy(all_useful_rules)
          thread_snapshot = threading.Thread(target=self.process_snapshot_rule_exis_file, args=(snapshot_rules, snapshot_file, ))
          thread_snapshot.start()
          print('created snapshot {} after {} seconds'.format(total_rule, elapsed_seconds))
          print('*************************done learning*********************************')
          thread_snapshot.join()
          return 0
        batch_start_time = current_milli_time()
        while True:
          if current_milli_time() - batch_start_time > self.cfg['batch_time']:
            break
          path_counter += 1
          path = path_sampler.sample_triple(rule_size + 2, new_triple, mine_cyclic_not_acyclic)
          if path != None and path.is_valid():
            rule = Rule()
            rule.init_from_path(path)
            gen_rules = rule.get_generalizations(mine_cyclic_not_acyclic)
            for r in gen_rules:
              if r.is_trivial():
                continue
              batch_rules += 1
              if r not in useful_rules:
                r.compute_scores(triple_set)
              if r.confidence >= 0.45 and r.correctly_predicted >= self.cfg['threshold_correct_predictions']: #self.cfg['threshold_confidence']
                batch_new_useful_rules += 1
                useful_rules.add(r)
              else:
                batch_previously_found_rules += 1
        batch_counter += 1
        str_type = 'CYCLIC' if mine_cyclic_not_acyclic else 'ACYCLIC'
        print('=====> batch [{} {}] {} (sampled {} pathes) *****'.format(str_type, rule_size + 1, batch_counter, path_counter))
        if batch_new_useful_rules + batch_previously_found_rules != 0:
          current_coverage = batch_previously_found_rules / (batch_new_useful_rules + batch_previously_found_rules)
        else:
          current_coverage = 0
        print('=====> fraction of previously seen rules within useful rules in this batch: {} num of new rule = {} num of previously rule = {} num of all batch rules = {}'.format(current_coverage,batch_new_useful_rules, batch_previously_found_rules, batch_rules))
        print('=====> stored rules: {}'.format(len(useful_rules)))
        if mine_cyclic_not_acyclic:
          last_cyclic_coverage = current_coverage
        else:
          last_cyclic_coverage = current_coverage

        if current_coverage > self.cfg['saturation'] and batch_previously_found_rules > 1:
          rule_size += 1
          if mine_cyclic_not_acyclic:
            rule_size_cyclic = rule_size
          if not mine_cyclic_not_acyclic:
            rule_size_acyclic = rule_size
          print('=========================================================')
          print('=====> increasing rule size of {} rule to {}'.format(str_type, rule_size + 1))
          self.log.info('increasing rule size of {} rules to {}  after {} s'.format(str_type, rule_size + 1, (current_milli_time() - start_time)//1000))
          all_useful_rules.append(set())

        mine_cyclic_not_acyclic = not mine_cyclic_not_acyclic
        if mine_cyclic_not_acyclic and rule_size_cyclic + 1 > self.cfg['max_length_cylic']:
          mine_cyclic_not_acyclic = False