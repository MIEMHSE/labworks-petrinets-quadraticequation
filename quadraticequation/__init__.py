#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Sergey Sobko'
__email__ = 'S.Sobko@profitware.ru'
__copyright__ = 'Copyright 2014, The Profitware Group'

from math import sqrt

from snakes.nets import *
import snakes.plugins
snakes.plugins.load('gv', 'snakes.nets', 'nets')

from nets import *


def quadratic_equation_factory():
    n = PetriNet('QuadraticEquation')
    n.add_place(Place('a', [2]))
    n.add_place(Place('b', [3]))
    n.add_place(Place('c', [1]))

    transition_squared_b = Transition('b ^ 2 transition')
    n.add_transition(transition_squared_b)
    n.add_input('b', 'b ^ 2 transition', Variable('b'))
    n.add_place(Place('b ^ 2'))
    n.add_output('b ^ 2', 'b ^ 2 transition', Expression('b ** 2'))

    transition_ac4 = Transition('4 * a * c transition')
    n.add_transition(transition_ac4)
    n.add_input('a', '4 * a * c transition', Variable('a'))
    n.add_input('c', '4 * a * c transition', Variable('c'))
    n.add_place(Place('4 * a * c'))
    n.add_output('4 * a * c', '4 * a * c transition', Expression('4 * a * c'))

    transition_squared_b_minus_ac4 = Transition('b ^ 2 - 4 * a * c transition')
    n.add_transition(transition_squared_b_minus_ac4)
    n.add_input('b ^ 2', 'b ^ 2 - 4 * a * c transition', Variable('squared_b'))
    n.add_input('4 * a * c', 'b ^ 2 - 4 * a * c transition', Variable('ac4'))
    n.add_place(Place('b ^ 2 - 4 * a * c'))
    n.add_output('b ^ 2 - 4 * a * c', 'b ^ 2 - 4 * a * c transition', Expression('squared_b - ac4'))

    transition_squared_a4 = Transition('4 * a ^ 2 transition')
    n.add_transition(transition_squared_a4)
    n.add_input('a', '4 * a ^ 2 transition', Variable('a'))
    n.add_place(Place('4 * a ^ 2'))
    n.add_output('4 * a ^ 2', '4 * a ^ 2 transition', Expression('4 * a ** 2'))


    """
    n.add_place(Place('D'))


    n.add_input('a', 't', cons)
    n.add_output('tgt', 't', prod)
    """
    return n, [transition_ac4, transition_squared_b, transition_squared_b_minus_ac4]

net, transitions = quadratic_equation_factory()
net.draw('value-0.png')
#print modes
for trans in transitions:
    trans.fire(trans.modes()[0])
net.draw('value-1.png')