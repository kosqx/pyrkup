#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


from pyrkup.core import Node, NodeKind, Markup


# TODO:
# - escape text
# - formating of output (newline after certain tags)
# - extensions
# - img @height, @width, @alt (stripped of tags)
# - table: @align, @colspan


def parse_link(tag, attrs):
    return Node(NodeKind.LINK, {'address': dict(attrs)['href']}, [])

def parse_image(tag, attrs):
    return Node(NodeKind.IMAGE, {'address': dict(attrs)['src']}, [dict(attrs).get('alt')])

def parse_header(tag, attrs):
    return Node(NodeKind.HEADER, {'level': int(tag[-1])}, [])


TAG_TO_KIND = {
    'p': (NodeKind.PARAGRAPH, True),
    'blockquote': (NodeKind.BLOCKQUOTE, True),
    'pre': (NodeKind.RAW, True),
    'hr': (NodeKind.HORIZONTAL_RULE, False),

    'h1': (NodeKind.HEADER, parse_header),
    'h2': (NodeKind.HEADER, parse_header),
    'h3': (NodeKind.HEADER, parse_header),
    'h4': (NodeKind.HEADER, parse_header),
    'h5': (NodeKind.HEADER, parse_header),
    'h6': (NodeKind.HEADER, parse_header),

    'ol': (NodeKind.ORDERED_LIST, True),
    'ul': (NodeKind.UNORDERED_LIST, True),
    'li': (NodeKind.LIST_ITEM, True),

    'dl': (NodeKind.DEFINITION_LIST, True),
    'dt': (NodeKind.DEFINITION_TERM, True),
    'dd': (NodeKind.DEFINITION_DESCRIPTION, True),

    'table': (NodeKind.TABLE, True),
    'tr': (NodeKind.TABLE_ROW, True),
    'td': (NodeKind.TABLE_CELL, True),

    'a': (NodeKind.LINK, parse_link),
    'img': (NodeKind.IMAGE, parse_image),

    'strong': (NodeKind.BOLD, True),
    'em': (NodeKind.ITALIC, True),
    'tt': (NodeKind.MONOSPACE, True),
    'sub': (NodeKind.SUBSCRIPT, True),
    'sup': (NodeKind.SUPERSCRIPT, True),
    'u': (NodeKind.UNDERLINE, True),
    'strike': (NodeKind.STRIKETHROUGH, True),
    'br': (NodeKind.NEWLINE, False),
}


class PyrkupHtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag in TAG_TO_KIND:
            kind, func = TAG_TO_KIND[tag]
            if callable(func):
                new = func(tag, attrs)
            else:
                new = Node(kind, None, [] if func else None)
        else:
            new = Node(tag, None, [])
        self.stack[-1].data.append(new)
        self.stack.append(new)
    def handle_endtag(self, tag):
        self.stack.pop()
    def handle_data(self, data):
        self.stack[-1].data.append(data)


class HtmlMarkup(Markup):
    auto_format_table = {
        NodeKind.PARAGRAPH: (u'<p>', u'</p>'),
        NodeKind.BLOCKQUOTE: (u'<blockquote>', u'</blockquote>'),
        NodeKind.HEADER: lambda n: ('<h%d>' % n.attr['level'], '</h%d>' % n.attr['level']),
        NodeKind.RAW: lambda n: '<pre>%s</pre>' % (u''.join(n.data)),
        NodeKind.HORIZONTAL_RULE: u'<hr />',

        NodeKind.ORDERED_LIST: (u'<ol>', u'</ol>'),
        NodeKind.UNORDERED_LIST: (u'<ul>', u'</ul>'),
        NodeKind.LIST_ITEM: (u'<li>', u'</li>'),

        NodeKind.DEFINITION_LIST: (u'<dl>', u'</dl>'),
        NodeKind.DEFINITION_TERM: (u'<dt>', u'</dt>'),
        NodeKind.DEFINITION_DESCRIPTION: (u'<dd>', u'</dd>'),

        NodeKind.TABLE: (u'<table>', u'</table>'),
        NodeKind.TABLE_ROW: (u'<tr>', u'</tr>'),
        NodeKind.TABLE_CELL: (u'<td>', u'</td>'),

        NodeKind.LINK: lambda n: ('<a href="%s">' % n.attr['address'], '</a>'),
        NodeKind.IMAGE: lambda n: '<img src="%s" alt="%s" />' % (n.attr['address'], u''.join(n.data)),

        NodeKind.BOLD: (u'<strong>', u'</strong>'),
        NodeKind.ITALIC: (u'<em>', u'</em>'),
        NodeKind.MONOSPACE: (u'<tt>', u'</tt>'),
        NodeKind.SUBSCRIPT: (u'<sub>', u'</sub>'),
        NodeKind.SUPERSCRIPT: (u'<sup>', u'</sup>'),
        NodeKind.UNDERLINE: (u'<u>', u'</u>'),
        NodeKind.STRIKETHROUGH: (u'<strike>', u'</strike>'),
        NodeKind.NEWLINE: u'<br />',
    }

    def format(self, node):
        return self.auto_format(node)

    def parse(self, text):
        parser = PyrkupHtmlParser()
        parser.stack = [Node(None, {}, [])]
        parser.feed(text)
        return parser.stack[0].data
