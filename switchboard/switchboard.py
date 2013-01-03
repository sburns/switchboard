#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views.py

Main routing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from flask import Blueprint, request, current_app, g

from .operator import Operator

switchboard = Blueprint('switchboard', __name__)


@switchboard.before_request
def add_operator():
    g.op = Operator(current_app.config.get('SWITCHBOARD', []))


@switchboard.route('/', methods=['GET', 'POST'])
def trigger():
    if request.method == 'POST':
        data = extract(request.form)
        g.op.connect(data)
        return 'Thank you', 200
    if request.method == 'GET':
        return "I'm expecting a POST call, but this will have to do", 200


def extract(form):
    """ Logic for breaking down the POST form from redcap """
    d = {}
    d['pid'] = int(request.form.get('project_id', 0))
    d['form'] = request.form.get('instrument', '')
    d['record'] = request.form.get('record', '')
    d['event'] = request.form.get('redcap_event_name', '')
    d['dag'] = request.form.get('redcap_data_access_group', '')
    d['status'] = int(request.form.get(comp_key(d['form']), 0))
    return d


def comp_key(inst):
    """Transforms the name of the instrument into a key that can be used
    to look up the form's complete status"""
    return '{0}_complete'.format(inst.lower())
