#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


import pytest


from pyrkup.core import Node, NodeKind
from pyrkup.markup.html import HtmlMarkup




def v(kind):
    return [u'foo ', Node(kind, None, [u'bar']), ' baz']


DATA_TABLE_HTML = u''.join([
    u'<table>',
    u'<tr><td>foo</td><td>bar</td></tr>'
    u'<tr><td>baz</td><td>qux</td></tr>'
    u'</table>'
])
DATA_TABLE_NODES = [Node(NodeKind.TABLE, None, [
    Node(NodeKind.TABLE_ROW, None, [
        Node(NodeKind.TABLE_CELL, None, [u'foo']),
        Node(NodeKind.TABLE_CELL, None, [u'bar']),
    ]),
    Node(NodeKind.TABLE_ROW, None, [
        Node(NodeKind.TABLE_CELL, None, [u'baz']),
        Node(NodeKind.TABLE_CELL, None, [u'qux']),
    ]),
])]


DATA_ORDERED_HTML = u''.join([
    u'<ol>',
    u'<li>foo</li>'
    u'<li>bar</li>'
    u'</ol>'
])
DATA_ORDERED_NODES = [Node(NodeKind.ORDERED_LIST, None, [
    Node(NodeKind.LIST_ITEM, None, [u'foo']),
    Node(NodeKind.LIST_ITEM, None, [u'bar']),
])]


DATA_UNORDERED_HTML = u''.join([
    u'<ul>',
    u'<li>foo</li>'
    u'<li>bar</li>'
    u'</ul>'
])
DATA_UNORDERED_NODES = [Node(NodeKind.UNORDERED_LIST, None, [
    Node(NodeKind.LIST_ITEM, None, [u'foo']),
    Node(NodeKind.LIST_ITEM, None, [u'bar']),
])]


DATA_DEFINITION_HTML = u''.join([
    u'<dl>',
    u'<dt>foo</dt>'
    u'<dd>bar</dd>'
    u'</dl>'
])
DATA_DEFINITION_NODES = [Node(NodeKind.DEFINITION_LIST, None, [
    Node(NodeKind.DEFINITION_TERM, None, [u'foo']),
    Node(NodeKind.DEFINITION_DESCRIPTION, None, [u'bar']),
])]


DATA = [
    (u'foo <p>bar</p> baz', v(NodeKind.PARAGRAPH)),
    (u'foo <blockquote>bar</blockquote> baz', v(NodeKind.BLOCKQUOTE)),
    (u'foo <h1>bar</h1> baz', [u'foo ', Node(NodeKind.HEADER, {'level': 1}, [u'bar']), u' baz']),
    (u'foo <pre>bar</pre> baz', v(NodeKind.RAW)),
    (u'foo <hr /> baz', [u'foo ', Node(NodeKind.HORIZONTAL_RULE), u' baz']),

    (DATA_ORDERED_HTML, DATA_ORDERED_NODES),
    (DATA_UNORDERED_HTML, DATA_UNORDERED_NODES),
    (DATA_DEFINITION_HTML, DATA_DEFINITION_NODES),
    (DATA_TABLE_HTML, DATA_TABLE_NODES),

    (u'foo <a href="example.com">example.com</a> baz', [u'foo ', Node(NodeKind.LINK, {'address': u'example.com'}, [u'example.com']), u' baz']),
    (u'foo <a href="example.com">name</a> baz', [u'foo ', Node(NodeKind.LINK, {'address': u'example.com'}, [u'name']), u' baz']),

    (u'foo <img src="example.jpg" alt="example" /> baz', [u'foo ', Node(NodeKind.IMAGE, {'address': u'example.jpg'}, [u'example']), u' baz']),

    (u'foo <strong>bar</strong> baz', v(NodeKind.BOLD)),
    (u'foo <em>bar</em> baz', v(NodeKind.ITALIC)),
    (u'foo <tt>bar</tt> baz', v(NodeKind.MONOSPACE)),
    (u'foo <sub>bar</sub> baz', v(NodeKind.SUBSCRIPT)),
    (u'foo <sup>bar</sup> baz', v(NodeKind.SUPERSCRIPT)),
    (u'foo <u>bar</u> baz', v(NodeKind.UNDERLINE)),
    (u'foo <strike>bar</strike> baz', v(NodeKind.STRIKETHROUGH)),

    (u'foo<br />bar', [u'foo', Node(NodeKind.NEWLINE), u'bar']),
]


@pytest.mark.parametrize(('text', 'nodes'), DATA)
def test_parse(text, nodes):
    print(HtmlMarkup().parse(text))
    print(nodes)
    assert HtmlMarkup().parse(text) == nodes


@pytest.mark.parametrize(('text', 'nodes'), DATA)
def test_format(text, nodes):
    print(HtmlMarkup().format(nodes))
    print(text)
    assert HtmlMarkup().format(nodes) == text
