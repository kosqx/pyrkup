#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


from pyrkup.core import Node, Markup


class CreoleMarkup(Markup):
    auto_format_table = {
        'para': (u'', u'\n\n'),
        'bold': (u'**', u'**'),
    }

    def format(self, node):
        return self.auto_format(node)

    def parse(self, text):
        pass
