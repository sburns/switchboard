#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

Main switchboard app
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from flask import Flask
app = Flask(__name__)

from . import views