#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


import pytest


from pyrkup.core import Node

from pyrkup.markup.creole import CreoleMarkup
from pyrkup.markup.html import HtmlMarkup

from pyrkup.markup.creole import creole_parse, build_tree


data = Node('para', None, [
    'foo',
    Node('bold', None, [
        'bar',
    ]),
])


def test_html_format():
    html = HtmlMarkup()
    assert html.format(data) == u'<p>foo<strong>bar</strong></p>'


def test_creole_format():
    creole = CreoleMarkup()
    assert creole.format(data) == u'foo**bar**\n\n'


def test_creole_parse():
    creole = CreoleMarkup()
    assert creole.parse(u'foo**bar**') == [
        u'foo',
        Node('bold', None, [
            u'bar',
        ])
    ]


creole_parse_result = [
    ('text', u'foo'),
    ('start', 'bold'),
    ('text', u'bar'),
    ('stop', 'bold'),
]


def test_creole_parse_fn():
    result = creole_parse(u'foo**bar**')
    assert result == creole_parse_result


def test_build_tree_fn():
    result = build_tree(creole_parse_result)
    assert result == [
        u'foo',
        Node(kind='bold', attr=None, data=[u'bar'])
    ]
