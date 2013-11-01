#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


from pyrkup.core import Node, Markup


class HtmlMarkup(Markup):
    auto_format_table = {
        'para': (u'<p>', u'</p>'),
        'bold': (u'<b>', u'</b>'),
    }

    def format(self, node):
        return self.auto_format(node)

    def parse(self, text):
        pass
