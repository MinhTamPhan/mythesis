# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file TripleSet.java
from .triple import Triple

class TripleSet (object):

  def __init__(self):
    self.triples = []

    self.head_to_list = {}
    self.tail_to_list = {}
    self.relation_to_list = {}

    self.head_relation_to_tail = {}
    self.head_tail_to_relation = {}
    self.tail_relation_to_head = {}

    self.frequent_relations = set([])

  def read_triples(self, filepath):
    with open(filepath, encoding='utf-8') as files:
      lineCounter = 0
      for line in files:
        line = line.strip()
        lineCounter += 1
        if lineCounter % 1000000 == 0:
          print('>>> parsed {0} lines'.format(lineCounter))
        token = line.split('\t')

        if len(token) < 3:
          token = line.split(' ')

        if len(token) == 3:
          triple = Triple(token[0], token[1], token[2])
          self.triples.append(triple)
      self.__index_triples()

  def __index_triples(self):
    counter = 0
    for triple in self.triples:
      counter += 1
      if counter % 100000 == 0:
        print('* indexed {} triples'.format(counter))
      self.__add_triple_to_index(triple)
    print('* set up index for {} relations, {} head entities, and {} tail entities'.format(len(self.relation_to_list.keys()), len(self.head_to_list.keys()), len(self.tail_to_list.keys())));

  def get_triples_by_head(self, head):
    res = self.head_to_list.get(head)
    if res == None:
      return []
    return res

  def get_triples_by_tail(self, tail):
    res = self.tail_to_list.get(tail)
    if res == None:
      return []
    return res

  def get_triples_by_relation(self, relation):
    if relation in self.relation_to_list:
      return self.relation_to_list.get(relation)
    else:
      return []

  def get_tail_entities(self, relation, head):
    if head in self.head_relation_to_tail:
      if relation in self.head_relation_to_tail.get(head):
        return self.head_relation_to_tail.get(head).get(relation)
    return set([])

  def get_head_entities(self, relation, tail):
    if tail in self.tail_relation_to_head:
      if relation in self.tail_relation_to_head.get(tail):
        return self.tail_relation_to_head.get(tail).get(relation)
    return set([])

  def is_true(self, head, relation, tail):

    if tail in self.tail_relation_to_head:
      if relation in self.tail_relation_to_head.get(tail):
        # if head in self.tail_relation_to_head.get(tail).get(relation):
        #   print(head, self.tail_relation_to_head.get(tail).get(relation))
        return head in self.tail_relation_to_head.get(tail).get(relation)
    return False

  def add_triple_set(self, triple_set):
    for triple in triple_set.triples:
      self.triples.append(triple)
      self.__add_triple_to_index(triple)

  '''/**
	* Returns those values for which the relation holds for a given value. If the headNotTail is
	* set to true, the value is interpreted as head value and the corresponding tails are returned.
	* Otherwise, the corresponding heads are returned.
	*
	* @param relation The specified relation.
	* @param value The value interpreted as given head or tail.
	* @param headNotTail Whether to interpret the value as head and not as tail (false interprets as tail).
	* @return The resulting values.
	*/'''

  def get_entities(self, relation, value, head_not_tail):
    if head_not_tail:
      return self.get_tail_entities(relation, value)
    else:
      return self.get_head_entities(relation, value)


  def __add_triple_to_index(self, triple):
    head = triple.head
    tail = triple.tail
    relation = triple.relation

    # index head
    if head not in self.head_to_list:
      self.head_to_list[head] = []
    self.head_to_list.get(head).append(triple)

    # index tail
    if tail not in self.tail_to_list:
      self.tail_to_list[tail] = []
    self.tail_to_list.get(tail).append(triple)

    # index relation
    if relation not in self.relation_to_list:
      self.relation_to_list[relation] = []
    self.relation_to_list.get(relation).append(triple)

    # index head-relation => tail
    if head not in self.head_relation_to_tail:
      self.head_relation_to_tail[head] = {}
    if relation not in self.head_relation_to_tail.get(head):
      self.head_relation_to_tail.get(head)[relation] = set([])
    self.head_relation_to_tail.get(head).get(relation).add(tail)

    # index tail-relation => head
    if tail not in self.tail_relation_to_head:
      self.tail_relation_to_head[tail] = {}
    if relation not in self.tail_relation_to_head.get(tail):
      self.tail_relation_to_head.get(tail)[relation] = set([])
    self.tail_relation_to_head.get(tail).get(relation).add(head)

    # index head-tail => relation
    if head not in self.head_tail_to_relation:
      self.head_tail_to_relation[head] = {}
    if tail not in self.head_tail_to_relation.get(head):
      self.head_tail_to_relation.get(head)[tail] = set([])
    self.head_tail_to_relation.get(head).get(tail).add(relation)


  def add_batch_triple(self, triple_set):
    is_connected = False
    for triple in triple_set.triples:
      head = triple.head
      tail = triple.tail
      if head in self.head_to_list and not is_connected:
        is_connected = True
      self.triples.append(triple)
      self.__add_triple_to_index(triple)
    return (is_connected, triple_set)

  def add_edge_triple(self, triple):
    is_connected = False
    head = triple.head
    tail = triple.tail
    if head in self.head_to_list and not is_connected:
      is_connected = True
    self.triples.append(triple)
    self.__add_triple_to_index(triple)
    return (is_connected, triple)