#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" core.py

Main switchboard classes
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'


class Operator(object):

    def __init__(self, workflows=None):
        self.workflows = workflows

    def connect(self, trigger):
        map(lambda x: x.handle(trigger), self.workflows)

    def __repr__(self):
        return "Operator<N=%d>" % len(self.workflows)


class Trigger(object):
    """Abstraction of incoming data entry trigger """
    keys = ['pid', 'form', 'status', 'dag', 'event', 'record']

    def __init__(self, pid=None, form=None, status=None, dag=None,
                 event=None, record=None):
        self.pid = pid
        self.form = form
        self.status = status
        self.dag = dag
        self.event = event
        self.record = record

    def __repr__(self):
        return 'Trigger<%s>' % ','.join([str(getattr(self, k)) for k in self.keys])

    def as_dict(self):
        return dict([(k, getattr(self, k)) for k in self.keys])


class Workflow(object):
    """ User-facing class from which workflows should inherit """
    pid = None
    form = None
    status = None
    dag = None
    event = None
    record = None

    def __init__(self):
        """Config comes from class variables"""
        pass

    def execute(self, trigger):
        """Subclasses should implement"""
        pass

    def handle(self, trigger):
        if self.does_match(trigger):
            self.execute(trigger)

    def does_match(self, trigger):
        attrs = ['pid', 'form', 'status', 'dag', 'event', 'record']
        for attr in attrs:
            val = getattr(self, attr)
            tvalue = getattr(trigger, attr)
            if (val is not None) and (tvalue is not None):
                if not self.match(val, tvalue):
                    return False
        return True

    @classmethod
    def match(self, value, trigger_value):
        """ Matching function """
        if isinstance(trigger_value, (int, long)):
            # If trigger is an int, try to coerce rec into int
            try:
                if int(value) == trigger_value:
                    return True
                else:
                    return False
            except TypeError:
                # List of ints?
                try:
                    int_list = map(int, value)
                    if trigger_value in int_list:
                        return True
                    else:
                        return False
                except (ValueError, TypeError):
                    return False
            except ValueError:
                return False
        if isinstance(trigger_value, basestring):
            if value == trigger_value:
                    return True
            else:
                # test if value is list
                if trigger_value in value:
                    return True
                else:
                    return False
