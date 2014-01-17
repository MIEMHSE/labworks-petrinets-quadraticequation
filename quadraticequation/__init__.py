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


def quadratic_equation_factory(**kwargs):
    n = PetriNet('QuadraticEquation')
    n.add_place(Place('a', map(float, kwargs['a'])))
    n.add_place(Place('b', map(float, kwargs['b'])))
    n.add_place(Place('c', map(float, kwargs['c'])))

    transition_concurrency_a = Transition('a concurrency transition')
    n.add_transition(transition_concurrency_a)
    n.add_input('a', 'a concurrency transition', Variable('a'))
    n.add_place(Place('a concurrent 1'))
    n.add_place(Place('a concurrent 2'))
    n.add_output('a concurrent 1', 'a concurrency transition', Variable('a'))
    n.add_output('a concurrent 2', 'a concurrency transition', Variable('a'))

    transition_concurrency_b = Transition('b concurrency transition')
    n.add_transition(transition_concurrency_b)
    n.add_input('b', 'b concurrency transition', Variable('b'))
    n.add_place(Place('b concurrent 1'))
    n.add_place(Place('b concurrent 2 minus'))
    n.add_place(Place('b concurrent 3 minus'))
    n.add_output('b concurrent 1', 'b concurrency transition', Variable('b'))
    n.add_output('b concurrent 2 minus', 'b concurrency transition', Expression('-b'))
    n.add_output('b concurrent 3 minus', 'b concurrency transition', Expression('-b'))

    transition_squared_b = Transition('b ^ 2 transition')
    n.add_transition(transition_squared_b)
    n.add_input('b concurrent 1', 'b ^ 2 transition', Variable('b'))
    n.add_place(Place('b ^ 2'))
    n.add_output('b ^ 2', 'b ^ 2 transition', Expression('b ** 2'))

    transition_ac4 = Transition('4 * a * c transition')
    n.add_transition(transition_ac4)
    n.add_input('a concurrent 1', '4 * a * c transition', Variable('a'))
    n.add_input('c', '4 * a * c transition', Variable('c'))
    n.add_place(Place('4 * a * c'))
    n.add_output('4 * a * c', '4 * a * c transition', Expression('4 * a * c'))

    transition_discriminant = Transition('discriminant transition')
    n.add_transition(transition_discriminant)
    n.add_input('b ^ 2', 'discriminant transition', Variable('squared_b'))
    n.add_input('4 * a * c', 'discriminant transition', Variable('ac4'))
    n.add_place(Place('discriminant'))
    n.add_output('discriminant', 'discriminant transition', Expression('squared_b - ac4'))

    transition_discriminant_squareroot = Transition('sqrt discriminant transition', Expression('discriminant >= 0'))
    n.add_transition(transition_discriminant_squareroot)
    n.add_input('discriminant', 'sqrt discriminant transition', Variable('discriminant'))
    n.add_place(Place('sqrt discriminant concurrent plus'))
    n.add_place(Place('sqrt discriminant concurrent minus'))
    n.add_output('sqrt discriminant concurrent plus', 'sqrt discriminant transition',
                 Expression('__import__("math").sqrt(discriminant)'))
    n.add_output('sqrt discriminant concurrent minus', 'sqrt discriminant transition',
                 Expression('- __import__("math").sqrt(discriminant)'))

    transition_a2 = Transition('2 * a transition')
    n.add_transition(transition_a2)
    n.add_input('a concurrent 2', '2 * a transition', Variable('a'))
    n.add_place(Place('2 * a concurrent 1'))
    n.add_place(Place('2 * a concurrent 2'))
    n.add_output('2 * a concurrent 1', '2 * a transition', Expression('2 * a'))
    n.add_output('2 * a concurrent 2', '2 * a transition', Expression('2 * a'))

    transition_numerator1 = Transition('-b + sqrt discriminant transition')
    n.add_transition(transition_numerator1)
    n.add_input('b concurrent 2 minus', '-b + sqrt discriminant transition', Variable('b'))
    n.add_input('sqrt discriminant concurrent plus', '-b + sqrt discriminant transition', Variable('sdp'))
    n.add_place(Place('numerator plus'))
    n.add_output('numerator plus', '-b + sqrt discriminant transition', Expression('b + sdp'))

    transition_numerator2 = Transition('-b - sqrt discriminant transition')
    n.add_transition(transition_numerator2)
    n.add_input('b concurrent 3 minus', '-b - sqrt discriminant transition', Variable('b'))
    n.add_input('sqrt discriminant concurrent minus', '-b - sqrt discriminant transition', Variable('sdm'))
    n.add_place(Place('numerator minus'))
    n.add_output('numerator minus', '-b - sqrt discriminant transition', Expression('b + sdm'))

    transition_x1 = Transition('x1 transition')
    n.add_transition(transition_x1)
    n.add_input('numerator plus', 'x1 transition', Variable('num'))
    n.add_input('2 * a concurrent 1', 'x1 transition', Variable('denom'))
    n.add_place(Place('x1'))
    n.add_output('x1', 'x1 transition', Expression('num / denom'))

    transition_x2 = Transition('x2 transition')
    n.add_transition(transition_x2)
    n.add_input('numerator minus', 'x2 transition', Variable('num'))
    n.add_input('2 * a concurrent 2', 'x2 transition', Variable('denom'))
    n.add_place(Place('x2'))
    n.add_output('x2', 'x2 transition', Expression('num / denom'))

    return n, [transition_concurrency_a,
               transition_concurrency_b,
               transition_ac4,
               transition_squared_b,
               transition_discriminant,
               transition_discriminant_squareroot,
               transition_a2,
               transition_numerator1,
               transition_numerator2,
               transition_x1,
               transition_x2]

if __name__ == '__main__':
    model_data = {
        'a': [1, 2],
        'b': [2, 3],
        'c': [1, 4]
    }
    steps = max(map(len, model_data.values()))
    net, transitions = quadratic_equation_factory(**model_data)
    net.draw('value-0.png')
    for step in range(0, steps):
        for trans in transitions:
            modes = trans.modes()
            if len(modes) > 0:
                trans.fire(modes[0])
        net.draw('value-%s.png' % (step + 1))