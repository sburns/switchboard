#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_operator.py

Testing switchboard.operator
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

import sys
sys.path.insert(0, '..')

from unittest import TestCase

from switchboard.operator import Operator


def dummy():
    pass

receivers = [{'pid': 1,
              'form': 'demographics',
              'status': 2,
              'func': dummy,
            },
             {'pid': [1, 2, 3],
              'form': ['demographics', 'imaging'],
              'status': [1, 2],
              'func': dummy,
              }]


class OperatorTest(TestCase):

    def setUp(self):
        self.op = Operator([])

    def tearDown(self):
        pass

    def test_matches(self):
        "Test matching function"
        matches = [(1, 1, True),
                   ('1', 1, True),
                   ([1], 1, True),
                   (['1'], 1, True),
                   (['1', 2], 2, True),
                   ([1, 2], 1, True),
                   ([1, 2], 0, False),
                   ([1, '2'], 0, False),
                   ('bar', 'bar', True),
                   (['foo', 'bar', 'bat'], 'bar', True),
                   (['foo', 'bar'], 'bat', False)]
        for i, match_data in enumerate(matches):
            rec_val, trig_val, good_result = match_data
            comp_result = self.op._matches(rec_val, trig_val)
            msg = "Match failure:"
            if good_result:
                msg += "(Should match but do not) "
            else:
                msg += "(Shouldn't match but do) "
            msg += 'match number %d' % i
            self.assertEqual(comp_result, good_result, msg)

    def test_filtering(self):
        """Test filtering receivers from triggers"""
        triggers = [(receivers[0], True, {'pid': 1, 'form': 'demographics', 'status': 2}),
                    (receivers[0], False, {'pid': 2, 'form': 'demographics', 'status': 2}),
                    (receivers[1], True, {'pid': 1, 'form': 'demographics', 'status': 2}),
                    (receivers[1], True, {'pid': 2, 'form': 'demographics', 'status': 2}),
                    (receivers[1], False, {'pid': 2, 'form': 'demographics', 'status': 0})]
        for i, trigger_data in enumerate(triggers):
            rec, good_match, data = trigger_data
            msg = "%d trigger failed" % i
            self.assertEquals(good_match, self.op._filter(rec, **data), msg)
