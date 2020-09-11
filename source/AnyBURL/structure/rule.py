# -*- coding: utf-8 -*-
# author: Phan Minh Tâm
# source has refer to java source of BURL method: http://web.informatik.uni-mannheim.de/AnyBURL/IJCAI/ijcai19.html file Rule.java
from structure.atom import Atom
from data.sampled_paired_result_set import SampledPairedResultSet
from structure.counter import Counter
from config.config_yaml import Config

class Rule(object):

  variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
  application_mode = False

  def __init__(self, head=None):
    self.cfg = Config.load_learning_config()
    self.cfg_predict = Config.load_predict_config()
    self.head = head
    self.body = []
    self.predicted = 0
    self.correctly_predicted = 0
    self.confidence = 0.0
    self.next_free_variable = 0
    self.hashcode = None

  def _check_values_and_variables(self, variables_this_to_other, variables_other_to_this, atom1, atom2, left_not_right):

    if atom1.is_LRC(left_not_right) and atom2.is_LRC(left_not_right):
      if not atom1.get_LR(left_not_right) == atom2.get_LR(left_not_right):
				# different constants in same position
        return False

    if atom1.is_LRC(left_not_right) != atom2.is_LRC(left_not_right):
			# one varaible and one constants do not fit
      return False

    if not atom1.is_LRC(left_not_right) and not atom2.is_LRC(left_not_right):
			# special cases X must be at same poistion as X, Y at same as Y
      if atom1.get_LR(left_not_right) == 'X' and not atom2.get_LR(left_not_right) == 'X':
        return False
      if atom2.get_LR(left_not_right) == 'X' and not atom1.get_LR(left_not_right) == 'X':
        return False

      if atom1.get_LR(left_not_right) == 'Y' and not atom2.get_LR(left_not_right) == 'Y':
        return False
      if atom2.get_LR(left_not_right) == 'Y' and not atom1.get_LR(left_not_right) == 'Y':
        return False

      if atom1.get_LR(left_not_right) in variables_this_to_other:
        that_varible = variables_this_to_other.get(atom1.get_LR(left_not_right))
        if not atom2.get_LR(left_not_right) == that_varible:
          return False

      if atom2.get_LR(left_not_right) in variables_this_to_other:
        this_varible = variables_this_to_other.get(atom2.get_LR(left_not_right))
        if not atom1.get_LR(left_not_right) == this_varible:
          return False

      if not atom1.get_LR(left_not_right) in variables_this_to_other:
        variables_this_to_other[atom1.get_LR(left_not_right)] = atom2.get_LR(left_not_right)
        variables_other_to_this[atom2.get_LR(left_not_right)] = atom1.get_LR(left_not_right)

    return True

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      if self.head == other.head:
        if len(self.body) == len(other.body):
          variables_this_to_other = {}
          variables_other_to_this = {}
          for i in range(len(self.body)):
            atom1 = self.body[i]
            atom2 = other.body[i]
            if not atom1.relation == atom2.relation:
              return False
            else:
              if not self._check_values_and_variables(variables_this_to_other, variables_other_to_this, atom1, atom2, True):
                return False
              if not self._check_values_and_variables(variables_this_to_other, variables_other_to_this, atom1, atom2, False):
                return False
        return True

    return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    body = ','.join([str(atom) for atom in self.body])
    return '{}\t{}\t{}\t{} <= {}'.format(self.predicted, self.correctly_predicted, self.confidence, self.head, body)

  def __hash__(self):
    if self.hashcode is None:
      string_repr = str(self.head)
      body = ''.join([b.relation for b in self.body])
      self.hashcode = hash(string_repr + body)
    return self.hashcode

  def init_from_path(self, path):
    self.body = []
    if path.markers[0] == '+' :
      self.head = Atom(path.nodes[0], path.nodes[1], path.nodes[2], True, True)
    else:
      self.head = Atom(path.nodes[2], path.nodes[1], path.nodes[0], True, True)

    for i in range(1, len(path.markers)):
      if path.markers[i] == '+':
        #print("markers size = " + p.markers.length + "   nodes size = " + p.nodes.length + "   i =" +  i)
        self.body.append(Atom(path.nodes[i * 2], path.nodes[i * 2 + 1], path.nodes[i * 2 + 2], True, True))
      else:
        self.body.append(Atom(path.nodes[i * 2 + 2], path.nodes[i * 2 + 1], path.nodes[i * 2], True, True))

  def init_measure(self, predicted, correctly_predicted, confidence):
    self.predicted = predicted
    self.correctly_predicted = correctly_predicted
    self.confidence = confidence

  def  is_XY_rule(self):
    return not self.head.is_left_constant and not self.head.is_right_constant

  def is_X_rule(self):
    if self.is_XY_rule():
      return False
    else:
      return not self.head.is_left_constant

  def is_Y_rule(self):
    if self.is_XY_rule():
      return False
    else:
      return not self.head.is_right_constant

  def __replace_by_variable(self, constant, variable):
    count = self.head.replace_by_variable(constant, variable)
    for batom in self.body:
      bcount = batom.replace_by_variable(constant, variable)
      count += bcount
    return count

  def __deep_copy(self):
    copy = Rule(self.head.clone())
    for body_literal in self.body:
      copy.body.append(body_literal.clone())
    copy.next_free_variable = self.next_free_variable
    return copy

  def __get_left_right_generalization(self):
    left_right_general = self.__deep_copy()
    left_constant = left_right_general.head.left
    xcount = left_right_general.__replace_by_variable(left_constant, 'X')
    right_constant = left_right_general.head.right
    ycount = left_right_general.__replace_by_variable(right_constant, 'Y')
    if xcount < 2 or ycount < 2:
      left_right_general = None
    return left_right_general

  def __replace_all_constants_by_variables(self):
    for atom in self.body:
      if atom.is_left_constant:
        c = atom.left
        self.__replace_by_variable(c, Rule.variables[self.next_free_variable])
        self.next_free_variable += 1
      if atom.is_right_constant:
        c = atom.right
        self.__replace_by_variable(c, Rule.variables[self.next_free_variable])
        self.next_free_variable += 1

  def __get_left_generalization(self):
    left_generalization = self.__deep_copy()
    left_constant = left_generalization.head.left
    x_count = left_generalization.__replace_by_variable(left_constant, 'X')
    if x_count < 2:
      left_generalization = None
    return left_generalization

  def __get_right_generalization(self):
    right_generalization = self.__deep_copy()
    right_constant = right_generalization.head.right
    y_count = right_generalization.__replace_by_variable(right_constant, 'Y')
    if y_count < 2:
      right_generalization = None
    return right_generalization

  def __replace_nearly_all_constants_by_variables(self):
    counter = 0
    for atom in self.body:
      counter += 1
      if counter == len(self.body):
        break
      if atom.is_left_constant:
        c = atom.left
        self.__replace_by_variable(c, Rule.variables[self.next_free_variable])
        self.next_free_variable += 1
      if atom.is_right_constant:
        c = atom.right
        self.__replace_by_variable(c, Rule.variables[self.next_free_variable]);
        self.next_free_variable += 1

  def get_generalizations(self, only_XY):
    generalizations = set([])
    left_right = self.__get_left_right_generalization()
    if left_right is not None:
      left_right.__replace_all_constants_by_variables()
      generalizations.add(left_right)

    if only_XY:
      return generalizations
    ## acyclic rule
    left = self.__get_left_generalization()
    if left is not None:
      left_free = left.__deep_copy()
      if left_right is None:
        left_free.__replace_all_constants_by_variables()
      left.__replace_nearly_all_constants_by_variables()
      generalizations.add(left)
      if left_right is None:
        generalizations.add(left_free)

    right = self.__get_right_generalization()
    if right is not None:
      right_free = right.__deep_copy()
      if left_right is None:
        right_free.__replace_all_constants_by_variables()
      right.__replace_nearly_all_constants_by_variables()
      generalizations.add(right)
      if left_right is None:
        generalizations.add(right_free)

    return generalizations

  def _get_cyclic(self, current_variable, last_variable, value, body_index, direction, triples, previous_values, final_results, counter):
		# print("currentVariable=" + current_variable + " lastVariable=" +  last_variable + " value=" + value + " bodyIndex=" + body_index)
    if Rule.application_mode and len(final_results) >= self.cfg['discrimination_bound']:
      final_results.clear()
      return

    if counter is not None:
      count = counter.incomming_and_get()
      if count >= self.cfg['trial_size']:
        return

    if not Rule.application_mode and len(final_results) >= self.cfg['sample_size']:
      return
    # check if the value has been seen before as grounding of another variable
    atom = self.body[body_index]
    head_not_tail = atom.left == current_variable
    if  value in previous_values:
      return
    # the current atom is the last
    if (direction == True and len(self.body) -1 == body_index) or (direction == False and body_index == 0):
      # get groundings
      for v in triples.get_entities(atom.relation, value, head_not_tail):
        if v not in previous_values:
          final_results.add(v)
      return
    ## the current atom is not the last
    else:
      results = triples.get_entities(atom.relation, value, head_not_tail)
      # print("atom.getRelation()=" + atom.relation + " value=" + value + " headNotTail=" + str(head_not_tail))
      next_variable = atom.right if head_not_tail else atom.left
      current_values = set(previous_values)
      current_values.add(value)
      i = 0
      for next_value in results:
        if not Rule.application_mode and i >= self.cfg['sample_size']:
          break
        updated_body_index =  body_index + 1 if direction else body_index - 1
        self._get_cyclic(next_variable, last_variable, next_value, updated_body_index, direction, triples, current_values, final_results, counter)
        i += 1
      return

  def ground_body_cyclic(self, first_variable, last_variable, triples, sampling_on=True):
    groundings = SampledPairedResultSet()
    atom = self.body[0]
    head_not_tail = atom.left == first_variable
    rtriples = triples.get_triples_by_relation(atom.relation)

    counter = 0
    count = Counter()
    for triple in rtriples:
      counter += 1
      last_variable_groundings = set([])
      triple_val = triple.get_value(head_not_tail)
      self._get_cyclic(first_variable, last_variable, triple_val, 0, True, triples, set([]), last_variable_groundings, count)
      if len(last_variable_groundings) > 0:
        if first_variable == 'X':
          groundings.add_key(triple_val)
          for last_variable_value in last_variable_groundings:
            groundings.add_value(last_variable_value)
        else:
          for last_variable_value in last_variable_groundings:
            groundings.add_key(last_variable_value)
            groundings.add_value(triple_val)
      if (counter >  self.cfg['sample_size'] or groundings.size() > self.cfg['sample_size']) and sampling_on:
        break
      if not Rule.application_mode and count.get() >= self.cfg['trial_size']:
        break
    return groundings

  def get_unbound_variable(self):
    if self.body[len(self.body) - 1].is_left_constant or self.body[len(self.body) - 1].is_right_constant:
      return None
    counter = {}
    for atom in self.body:
      if not atom.left == 'X' and not atom.left == 'Y':
        if atom.left in counter:
          counter[atom.left] = 2
        else:
          counter[atom.left] = 1

      if not atom.right == 'X' and not atom.right == 'X':
        if atom.right in counter:
          counter[atom.right] = 2
        else:
          counter[atom.right] = 1

    for key, value in counter.items():
      if value == 1:
        return key

    return None

  def forward_reversed(self, variable, value, body_index, target_variable, target_values={}, triple_set=set([]), previous_values={}):
    if value in previous_values:
      return
    if body_index < 0:
      target_values.add(value)
    else:
      current_values = set([value])
      atom = self.body[body_index]
      next_var_is_left = False
      if atom.left != variable:
        next_var_is_left = True
      next_variable = atom.get_LR(next_var_is_left)
      next_values = set([])
      if not Rule.application_mode and len(target_values) >= self.cfg['sample_size']:
        return
      # next_values.add()
      values_relation = triple_set.get_entities(atom.relation, value, not next_var_is_left)
      for v in values_relation:
        next_values.add(v)
      for next_value in next_values:
        self.forward_reversed(next_variable, next_value, body_index - 1, target_variable, target_values, triple_set, current_values)

  def compute_values_reversed(self, target_variable, target_values, triple_set):
    atom_index = len(self.body) - 1
    last_atom = self.body[atom_index]
    unbound_variable = self.get_unbound_variable()
    if unbound_variable is None:
      next_var_is_left = False
      if last_atom.is_right_constant:
        next_var_is_left = True
      constant = last_atom.get_LR(not next_var_is_left)
      next_variable = last_atom.get_LR(next_var_is_left)
      values = triple_set.get_entities(last_atom.relation, constant, not next_var_is_left)
      previous_values = set([])
      previous_values.add(constant)

      for value in values:
        self.forward_reversed(next_variable, value, atom_index - 1, target_variable, target_values, triple_set, previous_values)
        if not Rule.application_mode and len(target_values) >= self.cfg['sample_size']:
          return

        if Rule.application_mode and len(target_values) >=  self.cfg['discrimination_bound']:
          target_values.clear()
          return
    else :
      next_var_is_left = False
      if last_atom.left != unbound_variable:
        next_var_is_left = True
      next_variable = last_atom.get_LR(next_var_is_left)
      triples = triple_set.get_triples_by_relation(last_atom.relation)

      for triple in triples:
        value = triple.get_value(next_var_is_left)
        previous_values = set([])
        previous_value = triple.get_value(not next_var_is_left)
        previous_values.add(previous_value)
        self.forward_reversed(next_variable, value, atom_index - 1, target_variable, target_values, triple_set, previous_values)

        if not Rule.application_mode and len(target_values) >= self.cfg['sample_size']:
          return

        if Rule.application_mode and len(target_values) >= self.cfg['discrimination_bound']:
          target_values.clear()
          return

  def compute_scores(self, triples):
    if self.is_XY_rule():
			## X is given in first body atom
      xypairs = None
      is_zX = False
      for atom in self.body:
        if atom.left == 'X' or atom.right == 'X':
          is_zX = True
          break
      if is_zX:
        xypairs = self.ground_body_cyclic('X', 'Y', triples)
      else:
        xypairs = self.ground_body_cyclic('Y', 'X', triples)
      correctly_predicted, predicted = 0, 0
      for key, values in xypairs.values.items():
        for value in values:
          predicted += 1
          if triples.is_true(key, self.head.relation, value):
            correctly_predicted += 1

      self.predicted = predicted
      self.correctly_predicted = correctly_predicted
      self.confidence = correctly_predicted / predicted if predicted != 0 else 0
      # print('predicted={}, correctly_predicted={}, confidence={}'.format(predicted, correctly_predicted, self.confidence))
    if self.is_X_rule():
      xvalues = set([])
      self.compute_values_reversed('X', xvalues, triples)
      predicted, correctly_predicted = 0, 0
      for xvalue in xvalues:
        predicted += 1
        if triples.is_true(xvalue, self.head.relation, self.head.right):
          correctly_predicted += 1

      self.predicted = predicted
      self.correctly_predicted = correctly_predicted
      self.confidence = correctly_predicted / predicted

    if self.is_Y_rule():
      yvalues = set([])
      self.compute_values_reversed('Y', yvalues, triples)

      predicted , correctly_predicted = 0, 0
      for yvalue in yvalues:
        predicted += 1
        if triples.is_true(self.head.left, self.head.relation, yvalue):
          correctly_predicted += 1
      if predicted == 0:
        print('compute_values_reversed', yvalues)
      self.predicted = predicted
      self.correctly_predicted = correctly_predicted
      self.confidence = correctly_predicted / predicted

  def is_trivial(self):
    if len(self.body) == 1:
      if self.head == self.body[0]:
        return True
    return False

  def get_target_relation(self):
    return self.head.relation

  '''/**
	*  Returns the tail results of applying this rule to a given head value.
	*
	* @param head The given head value.
	* @param ts The triple set used for computing the results.
	* @return An empty set, a set with one value (the constant of the rule) or the set of all body instantiations.
	*/'''

  def compute_tail_results(self, head, triple_set):
    result_set = set([])
    if self.is_X_rule():
      if self.__is_body_true_acyclic('X', head, 0, triple_set):
        result_set.add(self.head.right)
        return result_set
    elif self.is_Y_rule():
      if self.head.left == head:
        self.compute_values_reversed('Y', result_set, triple_set)
        return result_set
    else:
      if len(self.body) > 3:
        return result_set
      results = set()
      count = Counter()
      # curr , last
      if self.body[0].contains('X'):
        self._get_cyclic('X', 'Y', head, 0, True, triple_set, set(), results, count)
      else:
        self._get_cyclic('X', 'Y', head, len(self.body) - 1, False, triple_set, set(), results, count)

      return results

    return result_set

  '''/**
	*  Returns the head results of applying this rule to a given tail value.
	*
	* @param tail The given tail value.
	* @param ts The triple set used for computing the results.
	* @return An empty set, a set with one value (the constant of the rule) or the set of all body instantiations.
	*/'''

  def compute_head_results(self, tail, triple_set):
    result_set = set([])
    if self.is_Y_rule():
      if self.__is_body_true_acyclic('Y', tail, 0, triple_set):
        result_set.add(self.head.left)
        return result_set
    elif self.is_X_rule():
      if self.head.right == tail:
        self.compute_values_reversed('X', result_set, triple_set)
        return result_set
    elif self.is_XY_rule():
      if len(self.body) > 3:
        return result_set
      results = set()
      count = Counter()
      if self.body[0].contains('Y'):
        self._get_cyclic('Y', 'X', tail, 0, True, triple_set,  set(), results, count)
      else:
        self._get_cyclic('Y', 'X', tail, len(self.body) - 1, False, triple_set, set(), results, count)
      return results
    return result_set

  def __is_body_true_acyclic(self, variable, value, body_index, triples):
    atom = self.body[body_index]
    head_not_tail = atom.left == variable
    # the current atom is the last
    if len(self.body) - 1 == body_index:
      constant = atom.is_right_constant if head_not_tail else atom.is_left_constant
      # get groundings, fixed by a constant
      if constant:
        constant_value = atom.get_LR(not head_not_tail)
        if head_not_tail:
          return triples.is_true(value, atom.relation, constant_value)
        else:
          return triples.is_true(constant_value, atom.relation, value)
      # existential quantification
      else:
        results = triples.get_entities(atom.relation, value, head_not_tail)
        if len(results) > 0:
          return True

      return False
    # the current atom is not the last
    else:
      results  = triples.get_entities(atom.relation, value, head_not_tail)
      next_variable = atom.get_LR(not head_not_tail)
      for next_val in results:
        if self.__is_body_true_acyclic(next_variable, next_val, body_index + 1, triples):
          return True

      return False

  def __get_cyclic(self, current_variable, last_variable, value, body_index, direction, triple_set, previous_values, final_results, counter):

    if Rule.application_mode and len(final_results) >=  self.cfg['discrimination_bound']:
      final_results.clear()

    if counter is not None:
      count = counter.incomming_and_get()
      if count >=  self.cfg['trial_size']:
        return
    if Rule.application_mode and len(final_results) >= self.cfg['sample_size']:
      return
    # check if the value has been seen before as grounding of another variable
    atom = self.body[body_index]
    head_not_tail = atom == current_variable
    if value in previous_values:
      return
    results = triples.get_entities(atom.relation, value, head_not_tail)
    if (direction == True and len(self.body) - 1 == body_index) or (direction == False and body_index == 0):
      for value in results:
        if value not in previous_values:
          final_results.add(value)
      return
    # the current atom is not the last
    else:
      next_variable = atom.get_LR(not head_not_tail)
      current_values = set(previous_values)
      current_values.add(value)
      i = 0
      for next_value in results:
        if not Rule.application_mode and i >= self.cfg['sample_size']:
          break
        updated_body_index = body_index + 1 if direction else body_index - 1
        self.__get_cyclic(next_variable, last_variable, next_value, updated_body_index, direction, triple_set, current_values, final_results, counter)
        i += 1

      return

  def get_applied_confidence(self):
    return self.correctly_predicted / (self.predicted + self.cfg_predict['unseen_nagative_examples'])

  def set_application_mode():
    Rule.application_mode = True

