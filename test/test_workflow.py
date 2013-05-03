#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_workflow.py

Testing switchboard.core.workflow
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

import sys
sys.path.insert(0, '..')

from unittest import TestCase

from switchboard import Workflow
from switchboard.core import Trigger


class Workflow1(Workflow):
    pid = 1
    form = 'demographics'
    status = 2

    def execute(self):
        pass


class Workflow2(Workflow):
    pid = [1, 2, 3]
    form = ['demographics', 'imaging']
    status = [1, 2]

    def execute(self):
        pass


class WorkflowTest(TestCase):

    def setUp(self):
        pass

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
            comp_result = Workflow.match(rec_val, trig_val)
            msg = "Match failure:"
            if good_result:
                msg += "(Should match but do not) "
            else:
                msg += "(Shouldn't match but do) "
            msg += 'match number %d' % i
            self.assertEqual(comp_result, good_result, msg)

    def test_filtering(self):
        """Test filtering workflows from triggers"""
        wf1 = Workflow1()
        wf2 = Workflow2()
        t1 = Trigger(pid=1, form='demographics', status=2)
        t2 = Trigger(pid=2, form='demographics', status=2)
        t3 = Trigger(pid=2, form='demographics', status=0)
        triggers = [(wf1, True, t1),
                    (wf1, False, t2),
                    (wf2, True, t1),
                    (wf2, True, t2),
                    (wf2, False, t3)]
        for i, trigger_data in enumerate(triggers):
            wf, good_match, trigger = trigger_data
            msg = "%d trigger failed" % i
            self.assertEquals(good_match, wf.does_match(trigger), msg)
