#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" operator.py

The operator connects calls to the right receivers
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from warnings import warn


class Operator(object):

    def __init__(self, receivers=None):
        self.init_receivers(receivers)

    def init_receivers(self, receivers):
        self.receivers = receivers

    def connect(self, trigger_info):
        good_recs = [r for r in self.receivers if self._filter(r, **trigger_info)]
        for rec in good_recs:
            if 'func' in rec:
                self._call(rec['func'], trigger_info)
            else:
                warn('No function found for a receiver')

    def _call(self, fxn, kwargs):
        """Abstract away from connect"""
        fxn(**kwargs)

    def _filter(self, rec, pid=None, form=None, status=None, dag=None,
        event=None, record=None):
        rec_vals = [rec.get('pid', None),
                    rec.get('form', None),
                    rec.get('status', None),
                    rec.get('dag', None),
                    rec.get('event', None),
                    rec.get('record', None)]
        trig_vals = [pid, form, status, dag, event, record]
        loop = zip(rec_vals, trig_vals)
        for rec_val, trig_val in loop:
            if (rec_val is not None) and (trig_val is not None):
                if not self._matches(rec_val, trig_val):
                    return False
        return True

    def _matches(self, rec_val, trigger_val):
        """ Matching function """
        if isinstance(trigger_val, (int, long)):
            # If trigger is an int, try to coerce rec into int
            try:
                if int(rec_val) == trigger_val:
                    return True
                else:
                    return False
            except TypeError:
                # List of ints?
                try:
                    int_list = map(int, rec_val)
                    if trigger_val in int_list:
                        return True
                    else:
                        return False
                except (ValueError, TypeError):
                    return False
            except ValueError:
                return False
        if isinstance(trigger_val, basestring):
            if rec_val == trigger_val:
                    return True
            else:
                # test if rec_val is list
                if trigger_val in rec_val:
                    return True
                else:
                    return False
