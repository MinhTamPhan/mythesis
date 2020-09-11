# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file ResultSet.java
from eval.completion_result import CompletionResult

class ResultSet(object):

  apply_threshold = False
  threshold = 0.0

  def __init__(self, name='', file_path='', contains_confidences=False, k=10):
    self.results = {}
    self.name = name
    self.file_path = file_path
    self.contains_confidences = contains_confidences
    self.k = k
    self.__init_from_file(file_path)

  def __init_from_file(self, file_path):
    reader = open(file_path)
    triple_line = reader.readline().strip('\n')
    i = 0
    while triple_line != None and len(triple_line) > 0:
      # if i % 1000:
      #   print('read line {} = {}'.format(i, triple_line))
      if len(triple_line) < 3:
        continue
      completion_result = CompletionResult(triple_line)
      head_line = reader.readline().strip('\n')
      tail_line = reader.readline().strip('\n')

      if head_line.find('Tails:') != -1:
        head_line, tail_line = tail_line, head_line

      if not ResultSet.apply_threshold:
        completion_result.add_head_results(self.__get_results_from_line(head_line[7:]), self.k)
        completion_result.add_tail_results(self.__get_results_from_line(tail_line[7:]), self.k)
      else:
        completion_result.add_head_results(self.__get_thresholded_results_from_line(head_line[7:]), self.k)
        completion_result.add_tail_results(self.__get_thresholded_results_from_line(tail_line[7:]), self.k)

      self.results[triple_line] = completion_result

      triple_line = reader.readline().strip('\n')
      i += 1

  def __get_results_from_line(self, rline):
    if not self.contains_confidences:
      return rline.split('\t')
    else:
      token = rline.split('\t')
      tokenx = []
      for i in range(0, len(token)//2):
        tokenx.append(token[i * 2])
      return tokenx

  def __get_thresholded_results_from_line(self, rline):
    if not self.containsConfidences:
      return rline.split('\t')
    else:
      t, cs = '', ''
      token = rline.split('\t')
      tokenx = []
      for i in range(0, len(token)/2):
        t = token[i * 2]
        cs = float(token[i * 2 + 1])
        if c > self.threshold:
          tokenx.append(t)
        else:
          break

      return tokenx

  def get_head_candidates(self, triple):
    if triple in self.results:
      return self.results.get(triple).head_results
    else:
      return []

  def get_tail_candidates(self, triple):
    if triple in self.results:
      return self.results.get(triple).tail_results
    else:
      return []