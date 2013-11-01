#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import


from pyrkup.core import Node

from pyrkup.markup.creole import CreoleMarkup
from pyrkup.markup.html import HtmlMarkup


data = Node('para', None, [
    'foo',
    Node('bold', None, [
        'bar',
    ]),
])


def main():
    html = HtmlMarkup()
    assert html.format(data) == u'<p>foo<b>bar</b></p>'
    creole = CreoleMarkup()
    assert creole.format(data) == u'foo**bar**\n\n'


if __name__ == '__main__':
    main()
