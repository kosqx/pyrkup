#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


from pyrkup.core import Node, NodeKind, Markup


# TODO:
# - escape text
# - formating of output (newline after certain tags)
# - extensions
# - img @height, @width, @alt (stripped of tags)
# - table: @align, @colspan


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
        pass
