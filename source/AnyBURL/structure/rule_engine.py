# from apply_config import ApplyConfig
from data.triple_set import TripleSet
from logger import Logger
from structure.score_tree import ScoreTree
from utilities import current_milli_time
import time
import heapq
import threading
import os

class RuleEngine(object):

  combination_rule_id = 1
  epsilon = 1e-4

  def __init__(self, output_path, unseen_nagative_example):
    if os.path.exists(output_path):
      os.remove(output_path)
    with open(output_path, 'w') as fp:
      pass
    self.output_path = output_path
    self.unseen_nagative_example = unseen_nagative_example
    self.log = Logger.get_log_cate('rule_engine.txt', 'RuleEngine')
    self.log.info('****************************start new section*************************************')
    self.log.info('initialize rule engine {}'.format(current_milli_time()))

  def apply_rules_arx(self, rules, training_set, test_set, validation_set, k):
    print('* applying rules')
    relation_to_rules = self.create_ordered_rule_index(rules)
    print('* set up index structure covering rules for {} different relations'.format(len(relation_to_rules)))
    filter_set = TripleSet()
    filter_set.add_triple_set(training_set)
    filter_set.add_triple_set(test_set)
    filter_set.add_triple_set(validation_set)
    print('* constructed filter set with {} triples'.format(len(filter_set.triples)))
    if len(filter_set.triples) == 0:
      print('WARNING: using empty filter set!')
    # prepare the data structures used a s cache for question that are reoccuring
    # start iterating over the test cases
    counter ,current_time, start_time = 0, 0, current_milli_time()

    ScoreTree.set_lower_bound(k)
    ScoreTree.set_upper_bound(ScoreTree.lower_bound)
    ScoreTree.set_epsilon(0.0001)

    for triple in test_set.triples:
      if counter % 100 == 0:
        print('* (# {} ) trying to guess the tail/head of {}'.format(counter, triple))
        current_time = current_milli_time()
        print('Elapsed (s) = {}'.format((current_time - start_time) // 1000))
        start_time = current_milli_time()
      relation = triple.relation
      head = triple.head
      tail = triple.tail
      tail_question, head_question = (relation, head), (relation, tail)
      k_tail_tree = ScoreTree()
      k_head_tree = ScoreTree()

      if relation in relation_to_rules:
        relevant_rules = relation_to_rules.get(relation)
        for rule in relevant_rules:
          if not k_tail_tree.fine():
            tail_candidates = rule.compute_tail_results(head, training_set)
            f_tail_candidates = self.__get_filtered_entities(filter_set, test_set, triple, tail_candidates, True)
            k_tail_tree.add_values(rule.get_applied_confidence(), f_tail_candidates)
          else:
            break
        for rule in relevant_rules:
          if not k_head_tree.fine():
            head_candidates = rule.compute_head_results(tail, training_set)
            f_head_candidates = self.__get_filtered_entities(filter_set, test_set, triple, head_candidates, False)
            k_head_tree.add_values(rule.get_applied_confidence(), f_head_candidates)
          else:
            break

      k_tail_candidates,k_head_candidates = {}, {}
      k_tail_tree.get_as_linked_map(k_tail_candidates)
      k_head_tree.get_as_linked_map(k_head_candidates)
      top_k_tail_candidates = self.__sort_by_value(k_tail_candidates, k)
      top_k_head_candidates = self.__sort_by_value(k_head_candidates, k)
      counter += 1
      writer = threading.Thread(target=self.__process_write_top_k_candidates, args=(triple, test_set, top_k_tail_candidates, top_k_head_candidates, ))
      writer.start()
    writer.join()
    print('* done with rule application')

  def create_ordered_rule_index(self, rules):
    relation_to_rules = {}
    while len(rules) > 0:
      rule = rules.pop()
      relation = rule.get_target_relation()
      if relation not in relation_to_rules:
        relation_to_rules[relation] = []
      relation_to_rules[relation].append(rule)

    for value in relation_to_rules.values():
      value.sort(key=lambda v: v.correctly_predicted / (v.predicted + self.unseen_nagative_example), reverse=True)

    return relation_to_rules

  def __get_filtered_entities(self, filter_set, test_set, triple, candidate_entities, tail_not_head):
    filtered_entities = set()
    for entity in candidate_entities:
      if not tail_not_head:
        if not filter_set.is_true(entity, triple.relation, triple.tail):
          filtered_entities.add(entity)
        if test_set.is_true(entity, triple.relation, triple.tail):
          if entity == triple.head:
            filtered_entities.add(entity)
      else:
        if not filter_set.is_true(triple.head, triple.relation, entity):
          filtered_entities.add(entity)
        if test_set.is_true(triple.head, triple.relation, entity):
          if entity == triple.tail:
            filtered_entities.add(entity)

    return filtered_entities

  # to do: implement heap
  def __sort_by_value(self, candidates, k):
    # heap = []
    res = []
    for key, val in candidates.items():
      res.append((key, val))
    res.sort(key=lambda item: item[1], reverse=True)
    return res[:k]

  def __process_write_top_k_candidates(self, triple, test_set, k_tail_candidates, top_k_head_candidates):
    with open(self.output_path, 'a') as output_stream:
      print('{}'.format(triple), file=output_stream)
      print('Heads: ', end='', file=output_stream)
      for (key, val) in top_k_head_candidates:
        if triple.head == key or not test_set.is_true(key, triple.relation, triple.tail):
          print('{}\t{}'.format(key, val), end='\t',file=output_stream)
      # print('\n', file=output)
      print('\nTails: ', end='', file=output_stream)
      for (key, val) in k_tail_candidates:
        if triple.tail == key or not test_set.is_true(triple.head, triple.relation, key):
          print('{}\t{}\t'.format(key, val), end='\t',file=output_stream)
      print('\n',end='', file=output_stream)