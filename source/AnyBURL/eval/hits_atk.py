# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file HitsAtK.java
class HitsAtK(object):

  atk_max = 100

  def __init__(self):
    self.filter_sets = []
    self.hits_adn_tail = [1 for i in range(100)]
    self.hits_adn_tail_filtered = [1 for i in range(100)]
    self.counter_tail = 0
    self.counter_tail_covered = 0
    self.head_ranks = []
    self.tail_ranks = []
    self.hits_adn_head = [1 for i in range(100)]
    self.hits_adn_head_filtered = [1 for i in range(100)]
    self.counter_head = 0
    self.counter_head_covered = 0

  def evaluate_head(self, candidates, triple):
    found_at = -1
    self.counter_head += 1
    if len(candidates) > 0:
      self.counter_head_covered += 1
    filter_count = 0
    rank = 0
    while rank < len(candidates) and rank < HitsAtK.atk_max:
      candidate = candidates[rank]
      if candidate == triple.head:
        for index in range(rank, self.atk_max):
          self.hits_adn_head[index] += 1
          self.hits_adn_head_filtered[index - filter_count] += 1
        found_at = rank + 1
        break
      else:
        for filter in self.filter_sets:
          if filter.is_true(candidate, triple.relation, triple.tail):
            filter_count += 1
            break
      rank += 1

    counter = 0
    ranked = False
    for candidate in candidates:
      counter += 1
      if candidate == triple.head:
        self.head_ranks.append(counter)
        ranked = True
        break
    if not ranked:
      self.head_ranks.append(-1)

    return found_at

  def evaluate_tail(self, candidates, triple):
    found_at = -1
    self.counter_tail += 1
    if len(candidates) > 0:
      self.counter_tail_covered += 1
    filter_count = 0
    rank = 0
    while rank < len(candidates) and rank < self.atk_max:
      candidate = candidates[rank]
      if candidate == triple.tail:
        for index in range(rank, self.atk_max):
          self.hits_adn_tail[index] += 1
          self.hits_adn_tail_filtered[index - filter_count] += 1
        found_at = rank + 1
        break
      else:
        for filter in self.filter_sets:
          if filter.is_true(triple.head, triple.relation, candidate):
            filter_count += 1

      rank += 1

    counter = 0
    ranked = False
    for candidate in candidates:
      counter += 1
      if candidate == triple.tail:
        self.tail_ranks.append(counter)
        ranked = True
        break
    if not ranked:
      self.tail_ranks.append(-1)
    return found_at