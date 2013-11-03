#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


import pytest


from pyrkup.core import Node, NodeKind
from pyrkup.markup.creole import CreoleMarkup, toplevel


def v(kind):
    return [u'foo ', Node(kind, None, [u'bar']), ' baz']


DATA = [
    (u'foo **bar** baz', v(NodeKind.BOLD)),
    (u'foo //bar// baz', v(NodeKind.ITALIC)),
    (u'foo ##bar## baz', v(NodeKind.MONOSPACE)),
    (u'foo ,,bar,, baz', v(NodeKind.SUBSCRIPT)),
    (u'foo ^^bar^^ baz', v(NodeKind.SUPERSCRIPT)),
    (u'foo __bar__ baz', v(NodeKind.UNDERLINE)),

    (u'foo\\\\bar', [u'foo', Node(NodeKind.NEWLINE), u'bar']),

    (u'foo{{{bar}}}baz', [u'foo', Node(NodeKind.RAW, None, [u'bar']), u'baz']),
    (u'foo{{{ **bar** }}}baz', [u'foo', Node(NodeKind.RAW, None, [u' **bar** ']), u'baz']),

    (u'foo[[example.com]]baz', [u'foo', Node(NodeKind.LINK, {'address': u'example.com'}, [u'example.com']), u'baz']),
    (u'foo[[example.com|name]]baz', [u'foo', Node(NodeKind.LINK, {'address': u'example.com'}, [u'name']), u'baz']),
]


@pytest.mark.parametrize(('text', 'nodes'), DATA)
def test_parse(text, nodes):
    print(CreoleMarkup().parse(text))
    print(nodes)
    assert CreoleMarkup().parse(text) == nodes


@pytest.mark.parametrize(('text', 'nodes'), DATA)
def test_format(text, nodes):
    print(CreoleMarkup().format(nodes))
    print(text)
    assert CreoleMarkup().format(nodes) == text

def test_toplevel():
    assert toplevel('''
= foo

* a
** aa
* b
** ba
additional line
** bb

== title
normal text

foo bar
baz quux
''') == [
        ['empty', '', ''],
        ['header', '= ', 'foo'],
        ['empty', '', ''],
        ['unordered', '* ', 'a'],
        ['unordered', '** ', 'aa'],
        ['unordered', '* ', 'b'],
        ['unordered', '** ', 'ba', 'additional line'],
        ['unordered', '** ', 'bb'],
        ['empty', '', ''],
        ['header', '== ', 'title'],
        ['text', '', 'normal text'],
        ['empty', '', ''],
        ['text', '', 'foo bar', 'baz quux'],
    ]
