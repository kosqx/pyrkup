#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


class Node(object):
    def __init__(self, kind, attr=None, data=None):
        self.kind = kind
        self.attr = attr
        self.data = data


class Markup(object):
    def format(self, data):
        pass

    def parse(self, text):
        pass
