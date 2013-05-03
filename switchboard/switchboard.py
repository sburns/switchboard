#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views.py

Main routing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from flask import Blueprint, request, current_app

from .core import Operator, Trigger

switchboard = Blueprint('switchboard', __name__)


@switchboard.route('/', methods=['GET', 'POST'])
def trigger():
    if request.method == 'POST':
        op = Operator(current_app.config.get('SWITCHBOARD_WORKFLOWS', []))
        trigger = trigger_from_form(request.form)
        op.connect(trigger)
        return 'Thank you', 200
    if request.method == 'GET':
        return "I'm expecting a POST call, but this will have to do", 200


def trigger_from_form(form):
    """ Logic for breaking down the POST form from redcap """
    data = dict(
                pid=int(form.get('project_id', 0)),
                form=form.get('instrument', ''),
                record=form.get('record', ''),
                event=form.get('redcap_event_name', ''),
                dag=form.get('redcap_data_access_group', ''),
                )
    data['status'] = int(form.get(comp_key(data['form']), 0))
    return Trigger(**data)


def comp_key(inst):
    """Transforms the name of the instrument into a key that can be used
    to look up the form's complete status"""
    return '{0}_complete'.format(inst.lower())
