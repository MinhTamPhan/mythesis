# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file Counter.java
class Counter(object):

  def __init__(self):
    self.counter = 0

  def incomming(self):
    self.counter += 1

  def get(self):
    return self.counter

  def incomming_and_get(self):
    self.counter += 1
    return self.counter