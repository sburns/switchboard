#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'
__version__ = '0.1'

from .core import Workflow
from .switchboard import switchboard


class Switchboard(object):
    def __init__(self, app, url_prefix='/trigger'):
        self.init_app(app, url_prefix)

    def init_app(self, app, url_prefix):
        app.register_blueprint(switchboard, url_prefix=url_prefix)
