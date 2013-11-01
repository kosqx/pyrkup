#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


from pyrkup.core import Node, Markup


class HtmlMarkup(Markup):
    def format(self, node):
        if isinstance(node, str):
            return unicode(node, 'utf-8')
        elif isinstance(node, unicode):
            return node
        elif isinstance(node, Node):
            if node.kind == 'para':
                return u'<p>' + u''.join(self.format(i) for i in node.data) + u'</p>'
            elif node.kind == 'bold':
                return u'<b>' + u''.join(self.format(i) for i in node.data) + u'</b>'
            else:
                raise ValueError('unsupported node kind: %r' % node.kind)
        else:
            raise TypeError('unsupported node type: %r' % type(node))

    def parse(self, text):
        pass
