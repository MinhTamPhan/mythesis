# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file CompletionResult.java

class CompletionResult(object):

  def __init__(self, triple):
    self.triple = triple
    self.head_results = []
    self.tail_results = []

  def add_head_results(self, heads, k):
    if k > 0:
      self.add_results(heads, self.head_results, k)
    else:
      self.add_results(heads, self.headResults)

  def add_tail_results(self, tails, k):
    if k > 0:
      self.add_results(tails, self.tail_results, k)
    else:
      self.add_results(tails, self.tail_results)

  def add_results(self, candidates, results, k=None):
    if k != None:
      for candidate in candidates:
        if candidate != '':
          results.append(candidate)
          k -= 1
          if k == 0:
            return
    else:
      for candidate in candidates:
        if candidate != '':
          results.append(candidate)

  def __str__(self):
    return 'triple:{}\n{}{}'.format(self.triple, self.head_results, self.tail_results)