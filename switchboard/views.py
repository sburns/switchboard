#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views.py

Main routing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from flask import request

from . import app


@app.route('/in', methods=['GET', 'POST'])
def incoming():
    if request.method == 'POST':
        print request.headers
        data = {}
        data['pid'] = int(request.form.get('project_id', 0))
        data['inst'] = request.form.get('instrument', '')
        data['record'] = request.form.get('record', '')
        data['event'] = request.form.get('redcap_event_name', '')
        data['dag'] = request.form.get('redcap_data_access_group', '')
        data['complete'] = int(request.form.get(comp_key(data['inst']), 0))
        print '\n'.join(['%s:%s' % (k, v) for k, v in data.items()])
        return "THANK YOU"
    if request.method == 'GET':
        return "WHY HELLO"

def comp_key(inst):
    """Transforms the name of the instrument into a key that can be used
    to look up the form's complete status"""
    return '{0}_complete'.format(inst.lower())