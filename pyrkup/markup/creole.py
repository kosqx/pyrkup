#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


from pyrkup.core import Node, Markup


class CreoleMarkup(Markup):
    def format(self, node):
        if isinstance(node, str):
            return unicode(node, 'utf-8')
        elif isinstance(node, unicode):
            return node
        elif isinstance(node, Node):
            if node.kind == 'para':
                return u''.join(self.format(i) for i in node.data) + u'\n\n'
            elif node.kind == 'bold':
                return u'**' + u''.join(self.format(i) for i in node.data) + u'**'
            else:
                raise ValueError('unsupported node kind: %r' % node.kind)
        else:
            raise TypeError('unsupported node type: %r' % type(node))

    def parse(self, text):
        pass
