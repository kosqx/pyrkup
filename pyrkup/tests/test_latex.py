#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


import pytest


from pyrkup.core import Node, NodeKind
from pyrkup.markup.latex import LatexMarkup


def v(kind):
    return [u'foo ', Node(kind, None, [u'bar']), ' baz']


DATA_ORDERED_HTML = u''.join([
    u'\\begin{enumerate}\n',
    u'\\item foo\n',
    u'\\item bar\n',
    u'\\end{enumerate}\n',
])
DATA_ORDERED_NODES = [Node(NodeKind.ORDERED_LIST, None, [
    Node(NodeKind.LIST_ITEM, None, [u'foo']),
    Node(NodeKind.LIST_ITEM, None, [u'bar']),
])]


DATA_UNORDERED_HTML = u''.join([
    u'\\begin{itemize}\n',
    u'\\item foo\n',
    u'\\item bar\n',
    u'\\end{itemize}\n',
])
DATA_UNORDERED_NODES = [Node(NodeKind.UNORDERED_LIST, None, [
    Node(NodeKind.LIST_ITEM, None, [u'foo']),
    Node(NodeKind.LIST_ITEM, None, [u'bar']),
])]


DATA = [
    (u'foo \nbar\n\n baz', v(NodeKind.PARAGRAPH)),
    (u'foo \\begin{quote}bar\\end{quote} baz', v(NodeKind.BLOCKQUOTE)),
    (u'foo \\section{bar} baz', [u'foo ', Node(NodeKind.HEADER, {'level': 1}, [u'bar']), u' baz']),
    (u'foo \\begin{verbatim}bar\\end{verbatim} baz', v(NodeKind.RAW)),
    (u'foo \\noindent\\makebox[\\linewidth]{\\rule{\\textwidth}{1pt}} baz', [u'foo ', Node(NodeKind.HORIZONTAL_RULE), u' baz']),

    (DATA_ORDERED_HTML, DATA_ORDERED_NODES),
    (DATA_UNORDERED_HTML, DATA_UNORDERED_NODES),

    (u'foo \\href{example.com}{example.com} baz', [u'foo ', Node(NodeKind.LINK, {'address': u'example.com'}, [u'example.com']), u' baz']),
    (u'foo \\href{example.com}{name} baz', [u'foo ', Node(NodeKind.LINK, {'address': u'example.com'}, [u'name']), u' baz']),

    (u'foo \\includegraphics{example.jpg} baz', [u'foo ', Node(NodeKind.IMAGE, {'address': u'example.jpg'}, [u'example']), u' baz']),

    (u'foo \\textbf{bar} baz', v(NodeKind.BOLD)),
    (u'foo \\textit{bar} baz', v(NodeKind.ITALIC)),
    (u'foo \\texttt{bar} baz', v(NodeKind.MONOSPACE)),
    (u'foo \\textsubscript{bar} baz', v(NodeKind.SUBSCRIPT)),
    (u'foo \\textsuperscript{bar} baz', v(NodeKind.SUPERSCRIPT)),
    (u'foo \\underline{bar} baz', v(NodeKind.UNDERLINE)),
    (u'foo \\sout{bar} baz', v(NodeKind.STRIKETHROUGH)),

    (u'foo\\\\\nbar', [u'foo', Node(NodeKind.NEWLINE), u'bar']),
]

@pytest.mark.parametrize(('text', 'nodes'), DATA)
def test_format(text, nodes):
    print(LatexMarkup().format(nodes))
    print(text)
    assert LatexMarkup().format(nodes) == text
