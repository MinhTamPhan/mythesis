# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file ScoreTree.java

class ScoreTree(object):

  lower_bound = 10
  upper_bound = 10
  epsilon = 1e-4

  def __init__(self):
    self.score = 0.0
    self.children = []
    self.stored_values = None
    self.closed = False
    self.num_of_values = 0
    self.index = 0
    self.root = True

  def init_from_value(self, score, values):
    self.score = score
    self.children = []
    self.stored_values = set([])
    for v in values:
      self.stored_values.add(v)
    if len(self.stored_values) <= 1:
      self.closed = True
    self.num_of_values = len(values)
    self.root = False

  def add_values(self, score, values):
    self.__add_values_imp(score, values, 0)

  def fine(self):
    if self.root and len(self.children) > 0:
      i = self.children[len(self.children) - 1].index
      if i == ScoreTree.lower_bound:
        return self.is_first_unique()
    return False

  def is_first_unique(self):
    if len(self.children) == 0:
      return self.closed
    tree = self.children[0]
    while len(tree.children) > 0:
      tree = tree.children[0]

    return tree.closed

  def get_as_linked_map(self, linked_map={}):
    self.__get_as_linked_map_imp(linked_map, 0, 0)

  def set_lower_bound(lower):
    ScoreTree.lower_bound = lower

  def set_upper_bound(upper):
    ScoreTree.upper_bound = upper

  def set_epsilon(eps):
    ScoreTree.epsilon = eps

  def __get_as_linked_map_imp(self, linked_map, ps, level):
    if len(self.children) > 0:
      for child in self.children:
        if self.root:
          child.__get_as_linked_map_imp(linked_map, ps, level + 1)
        else:
          ps_updated = ps + (ScoreTree.epsilon ** (level - 1)) * self.score
          child.__get_as_linked_map_imp(linked_map, ps_updated, level + 1)

    if not self.root:
      ps_updated = ps + (ScoreTree.epsilon ** (level - 1)) * self.score
      for values in self.stored_values:
        linked_map[values] = ps_updated

  def __add_child(self, score, values, child_index):
    child = ScoreTree()
    child.init_from_value(score, values)
    child.index = child_index
    self.children.append(child)
    return child

  def __add_values_imp(self, score, values, counter):
    # go deep first
    for child in self.children:
      child.__add_values_imp(score, values, 0)
    # compare with stored values
    touched = set([])
    untouched = set([])
    if not self.root:
      touched = self.stored_values & values
      untouched = self.stored_values - values
      values -= touched
    # standard split
    if len(touched) > 0 and len(self.stored_values) > 1 and len(touched) < len(self.stored_values):
      child_index = self.index - len(untouched)
      if child_index >= ScoreTree.lower_bound:
        self.stored_values = touched
        self.index = child_index
        self.num_of_values -= len(untouched)
      else:
        self.stored_values = untouched
        self.__add_child(score, touched, child_index)

    # special case of adding new value, which happens only if the maximal number of values is not yet exceeded
    if self.root and len(values) > 0 and self.num_of_values < ScoreTree.lower_bound:
      self.__add_child(score, values, self.num_of_values + len(values))
      self.num_of_values += len(values)

    # try to set on closed if only 1 or less values are stored in this and in its children
    if self.stored_values == None or len(self.stored_values) <= 1:
      child_closed = True
      for child in self.children:
        if not child.closed:
          child_closed = False
          break
      self.closed = child_closed

  def __to_string(self, indent):
    rep = ''
    closing_sign = 'X' if self.closed else ''
    stored_values = ' '.join([s for s in self.stored_values]) if self.stored_values is not None else ' '
    child = ''.join([c.__to_string(indent + '    ') for c in self.children if c is not None]) if self.children is not None else ' '
    rep += '{}{} {} [{}]({}) -> {{ {} }}\n{}'.format(indent, closing_sign, self.score, self.index, self.num_of_values, stored_values, child)
    # for child in self.children:
    #   rep += child.__to_string(indent + '\t')
    return rep

  def __str__(self):
    return self.__to_string('')

## unit test

# if __name__ == '__main__':
#   tree = ScoreTree()
#   s1 = set(['a', 'b', 'c', 'd', 'd1', 'd2'])
#   tree.add_values(0.9, s1)
#   print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#   print(tree)
#   print('precise enough',tree.fine())
#   print('first unique',tree.is_first_unique())


#   s11=set(['aaa', 'bbb'])
#   tree.add_values(0.8999, s11)
#   print(len(tree.children))
#   print(tree)
#   print('precise enough',tree.fine())
#   print('first unique',tree.is_first_unique())
#   print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#   print(tree)
#   print('precise enough',tree.fine())
#   print('first unique',tree.is_first_unique())