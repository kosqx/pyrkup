#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


class Node(object):
    def __init__(self, kind, attr=None, data=None):
        self.kind = kind
        self.attr = attr
        self.data = data

    def __repr__(self):
        return 'Node(kind=%r, attr=%r, data=%r)' % (
            self.kind, self.attr, self.data
        )

    def __cmp__(self, other):
        if not isinstance(other, Node):
            raise TypeError
        return cmp(
            (self.kind, self.attr, self.data),
            (other.kind, other.attr, other.data)
        )


class NodeKind(object):
    PARAGRAPH = 'para'
    HEADER = 'header'
    RAW = 'raw'

    TABLE = 'table'
    TABLE_ROW = 'row'
    TABLE_CELL = 'cell'

    LINK = 'link'
    IMAGE = 'image'

    BOLD = 'bold'
    ITALIC = 'italic'
    MONOSPACE = 'mono'
    SUBSCRIPT = 'sub'
    SUPERSCRIPT = 'super'
    UNDERLINE = 'under'
    STRIKETHROUGH = 'strike'
    NEWLINE = 'newline'


class Markup(object):
    def auto_format(self, node):
        if isinstance(node, str):
            return unicode(node, 'utf-8')
        elif isinstance(node, unicode):
            return node
        elif isinstance(node, list):
            return u''.join(self.auto_format(i) for i in node)
        elif isinstance(node, Node):
            formatter = self.auto_format_table.get(node.kind)
            if callable(formatter):
                return formatter(node)
            if isinstance(formatter, tuple) and len(formatter) == 2:
                return formatter[0] + self.auto_format(node.data) + formatter[1]
            elif isinstance(formatter, unicode):
                return formatter
            else:
                raise ValueError('unsupported node kind: %r' % node.kind)
        else:
            raise TypeError('unsupported node type: %r' % type(node))

    def format(self, data):
        pass

    def parse(self, text):
        pass
