#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


from pyrkup import five


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
        return cmp(self.to_tuple(), other.to_tuple())

    def __eq__(self, other):
        if not isinstance(other, Node):
            raise TypeError
        return self.to_tuple() == other.to_tuple()

    def to_tuple(self):
        return (self.kind, self.attr, self.data)


class NodeKind(object):
    PARAGRAPH = 'para'
    BLOCKQUOTE = 'blockquote'
    HEADER = 'header'
    RAW = 'raw'
    HORIZONTAL_RULE = 'hr'

    ORDERED_LIST = 'ol'
    UNORDERED_LIST = 'ul'
    LIST_ITEM = 'li'

    DEFINITION_LIST = 'dl'
    DEFINITION_TERM = 'dt'
    DEFINITION_DESCRIPTION = 'dd'

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
        if isinstance(node, five.string_types):
            return five.force_unicode(node)
        elif isinstance(node, list):
            return u''.join(self.auto_format(i) for i in node)
        elif isinstance(node, Node):
            formatter = self.auto_format_table.get(node.kind)

            if callable(formatter):
                formatter = formatter(node)

            if isinstance(formatter, tuple) and len(formatter) == 2:
                return formatter[0] + self.auto_format(node.data) + formatter[1]
            elif isinstance(formatter, five.string_types):
                return five.force_unicode(formatter)
            else:
                raise ValueError('unsupported node kind: %r' % node.kind)
        else:
            raise TypeError('unsupported node type: %r' % type(node))

    def format(self, data):
        pass

    def parse(self, text):
        pass
