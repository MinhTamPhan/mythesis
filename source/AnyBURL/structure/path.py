# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file Path.java
class Path(object):

  def __init__(self, nodes, markers):
    self.nodes = nodes
    self.markers = markers

  def is_valid(self):
    '''Checks if a path is valid for strict object identity.
	    return False, if the x and y values appear at the wrong position in the path, or if the
	    same entities appears several times in the body part of the path.'''
    xconst = self.nodes[0]
    yconst = self.nodes[2]
    visited_entities = set([])

    for i in range(4, len(self.nodes) - 2, 2):
      if self.nodes[i] == xconst:
        return False
      if self.nodes[i] == yconst:
        return False

    for i in range(2, len(self.nodes), 2):
      if self.nodes[i] in visited_entities:
        return False
      visited_entities.add(self.nodes[i])

    return True

  def __marked_node_to_string(self, index):
    if index % 2 == 1:
      return self.markers[(index - 1) // 2] + self.nodes[index]
    else:
      return self.nodes[index]

  def __str__(self):
    return '->'.join([self.__marked_node_to_string(i) for i in range(len(self.nodes))])