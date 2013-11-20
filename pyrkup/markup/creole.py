#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


import re


from pyrkup.core import Node, NodeKind, Markup


def creole_parse(text):
    parts = re.split(r'(\[\[[^\]\|]+(?:\|[^\]]+)?\]\]|\{\{\{.*?\}\}\}|\*\*|//|##|,,|\^\^|__|\\\\)', text)
    tags = {
        '**': NodeKind.BOLD,
        '//': NodeKind.ITALIC,
        '##': NodeKind.MONOSPACE,
        ',,': NodeKind.SUBSCRIPT,
        '^^': NodeKind.SUPERSCRIPT,
        '__': NodeKind.UNDERLINE,
    }
    counts = dict((i, 0) for i in tags)

    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            if part:
                result.append(('text', part))
        elif part == '\\\\':
            result.append(('put', Node(NodeKind.NEWLINE)))
        elif part.startswith('{{{'):
            result.append(('put', Node(NodeKind.RAW, None, [part[3:-3]])))
        elif part.startswith('[['):
            link_parts = part[2:-2].split('|')
            link_href, link_desc = link_parts[0], link_parts[-1]
            result.append(('put', Node(NodeKind.LINK, {'address': link_href}, [link_desc])))
        else:
            result.append((['start', 'stop'][counts[part] % 2], tags[part]))
            counts[part] += 1
    return result


def build_tree(seq):
    stack = [Node(None, None, [])]
    for op, value in seq:
        if op in ('text', 'put'):
            stack[-1].data.append(value)
        elif op == 'start':
            new = Node(value, None, [])
            stack[-1].data.append(new)
            stack.append(new)
        elif op == 'stop':
            stack.pop()
    return stack[0].data


def creole_format_link(node):
    if node.data == [node.attr['address']]:
        return '[[%s]]' % node.attr['address']
    else:
        return '[[%s|%s]]' % (node.attr['address'], node.data[0])


regexp = lambda pattern: re.compile('^' + pattern)
toplevel_table = [
    ('header', regexp(r'={1,5} '), False),
    ('unordered', regexp(r'\s*\*{1,5} '), True),
    ('ordered', regexp(r'\s*#{1,5} '), True),
    ('quote', regexp(r'>+ '), True),
    ('hr', regexp(r'\s*-{4,}\s?$'), False),
    ('table', regexp(r'\|'), False),

    ('empty', regexp(r'\s*$'), False),
]


def toplevel(text):
    def find(line):
        for name, regex, multiline in toplevel_table:
            m = regex.match(line)
            if m:
                return name, multiline, m.group(), line[len(m.group()):]
        return 'text', True, '', line

    result = []
    multi = False
    for line in text.splitlines():
        print(find(line))
        name, multiline, prefix, data = find(line)
        if name == 'text' and not multi:
            result.append(['text', '', data])
        elif name == 'text':
            result[-1].append(data)
        else:
            result.append([name, prefix, data])
        multi = multiline

    for i in result:
        print(i)

    return result


class CreoleMarkup(Markup):
    auto_format_table = {
        NodeKind.PARAGRAPH: (u'', u'\n\n'),
        NodeKind.RAW: (u'{{{', u'}}}'),

        NodeKind.LINK: creole_format_link,

        NodeKind.BOLD: (u'**', u'**'),
        NodeKind.ITALIC: (u'//', u'//'),
        NodeKind.MONOSPACE: (u'##', u'##'),
        NodeKind.SUBSCRIPT: (u',,', u',,'),
        NodeKind.SUPERSCRIPT: (u'^^', u'^^'),
        NodeKind.UNDERLINE: (u'__', u'__'),
        NodeKind.STRIKETHROUGH: (u'', u''),  # unsupported
        NodeKind.NEWLINE: u'\\\\',
    }

    def format(self, node):
        return self.auto_format(node)

    def parse(self, text):
        return build_tree(creole_parse(text))
