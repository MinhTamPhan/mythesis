# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file SampledPairedResultSet.java

class SampledPairedResultSet(object):
  def __init__(self):
    self.values = {}
    self.sampling = False
    self.value_counter = 0
    self.current_key = ''

  def add_key(self, key):
    self.current_key = key
    if key in self.values:
      return
    else:
      self.values[key] = set([])

  def add_value(self, value):
    self.values.get(self.current_key).add(value)
    self.value_counter += 1

  def size(self):
    return len(self.values)