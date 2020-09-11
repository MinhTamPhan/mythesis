# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file Atom.java

class Atom(object):

  def __init__(self, left=None, relation=None, right=None, is_left_constant=True, is_right_constant=True):
    self.left = left
    self.relation = relation
    self.right = right
    self.is_left_constant = is_left_constant
    self.is_right_constant = is_right_constant
    self.hashcode = None

  def from_atom_representation(self, string_atom=''):
    t1 = string_atom.split('(')
    # print(t1)
    t2 = t1[1].split(',')
    relation = t1[0]
    left = t2[0]
    right = t2[1][0 : len(t2[1]) - 1]
    if right[-1] == ')':
      right = right[0 : len(right) - 1]
    self.relation = relation
    self.left = left.strip()
    self.right = right.strip()
    self.is_left_constant = len(self.left) != 1
    self.is_right_constant = len(self.right) != 1

  def contains(self, term):
    return self.left == term or self.right == term

  def more_special(self, other):
    if isinstance(other, self.__class__):
      if self.relation == other.relation:
        if self == other:
          return True

        if self.left == other.left:
          if not other.is_right_constant and self.is_right_constant:
            return True
          return False

        if self.right == other.right:
          if not other.is_left_constant and self.is_left_constant:
            return True
          return False

        if not other.is_left_constant and not other.is_right_constant and self.is_left_constant and self.is_right_constant:
            return True
        return False
    else:
      return False

  def is_LRC(self, left_not_right):
    if left_not_right:
      return self.is_left_constant
    return self.is_right_constant

  def clone(self):
    return Atom(left=self.left, relation=self.relation, right=self.right, is_left_constant=self.is_left_constant, is_right_constant=self.is_right_constant)

  def replace_by_variable(self, constant='', variable=''):
    count = 0
    if self.is_left_constant and self.left == constant:
      self.is_left_constant = False
      self.left = variable
      count += 1
    if self.is_right_constant and self.right == constant:
      self.is_right_constant = False
      self.right = variable
      count += 1
    return count

  def get_LR(self, left_not_right):
    if left_not_right:
      return self.left
    else:
      return self.right

  def __str__(self):
    return '{}({},{})'.format(self.relation, self.left, self.right.strip('\n'))

  # def __repr__(self):
  #   return (self.left, self.relation, self.right, self.is_left_constant, self.is_right_constant)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.relation == other.relation and self.left == other.left and self.right == other.right
    return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
    if self.hashcode is None:
      self.hashcode = hash(self.__str__())
    return self.hashcode
