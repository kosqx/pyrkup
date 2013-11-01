#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


import re


from pyrkup.core import Node, Markup


def creole_parse(text):
    parts = re.split(r'(\[\[[^\]\|]+(?:\|[^\]]+)?\]\]|\*\*|//|``|\\)', text)
    counts = {'**': 0, '//': 0, '``': 0}
    tags = {'**': 'bold', '//': 'italic', '``': 'mono'}
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            if part:
                result.append(('text', part))
        elif part == '\\':
            result.append(('put', Node('newline')))
        elif part.startswith('[['):
            link_parts = part[2:-2].split('|')
            link_href, link_desc = link_parts[0], link_parts[-1]
            result.append(('put', Node('link', {'address': link_href}, [link_desc])))
        else:
            result.append((['start', 'stop'][counts[part] % 2], tags[part]))
            counts[part] += 1
    return result


def build_tree(seq):
    stack = [Node(None, None, [])]
    for op, value in seq:
        print stack
        if op in ('text', 'put'):
            stack[-1].data.append(value)
        elif op == 'start':
            new = Node(value, None, [])
            stack[-1].data.append(new)
            stack.append(new)
        elif op == 'stop':
            stack.pop()
    return stack[0].data


creole_parse_result = creole_parse(u'foo**bar**')
assert creole_parse_result == [('text', u'foo'), ('start', 'bold'), ('text', u'bar'), ('stop', 'bold')]
build_tree = build_tree(creole_parse_result)
assert build_tree == [u'foo', Node(kind='bold', attr=None, data=[u'bar'])]


class CreoleMarkup(Markup):
    auto_format_table = {
        'para': (u'', u'\n\n'),
        'bold': (u'**', u'**'),
    }

    def format(self, node):
        return self.auto_format(node)

    def parse(self, text):
        return build_tree(creole_parse(text))
