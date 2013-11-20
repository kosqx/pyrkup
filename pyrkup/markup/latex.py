#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


from pyrkup.core import Node, NodeKind, Markup

# TODO:
# - \usepackage{hyperref}
# - \usepackage{graphicx}
# - \usepackage{fixltx2e}
# - \usepackage{ulem}


class LatexMarkup(Markup):
    auto_format_table = {
        NodeKind.PARAGRAPH: (u'\n', u'\n\n'),
        NodeKind.BLOCKQUOTE: (u'\\begin{quote}', u'\\end{quote}'),
        NodeKind.HEADER: lambda n: ([u'\\chapter{', u'\\section{', u'\\subsection{', u'\\subsubsection{', u'\paragraph{'][n.attr['level']], '}'),
        NodeKind.RAW: lambda n: u'\\begin{verbatim}%s\\end{verbatim}' % (u''.join(n.data)),
        NodeKind.HORIZONTAL_RULE: u'\\noindent\\makebox[\\linewidth]{\\rule{\\textwidth}{1pt}}',

        NodeKind.ORDERED_LIST: (u'\\begin{enumerate}\n', u'\\end{enumerate}\n'),
        NodeKind.UNORDERED_LIST: (u'\\begin{itemize}\n', u'\end{itemize}\n'),
        NodeKind.LIST_ITEM: (u'\item ', u'\n'),

        NodeKind.LINK: lambda n: (u'\\href{%s}{' % n.attr['address'], '}'),
        NodeKind.IMAGE: lambda n: u'\\includegraphics{%s}' % n.attr['address'],

        NodeKind.BOLD: (u'\\textbf{', u'}'),
        NodeKind.ITALIC: (u'\\textit{', u'}'),
        NodeKind.MONOSPACE: (u'\\texttt{', u'}'),
        NodeKind.SUBSCRIPT: (u'\\textsubscript{', u'}'),
        NodeKind.SUPERSCRIPT: (u'\\textsuperscript{', u'}'),
        NodeKind.UNDERLINE: (u'\\underline{', u'}'),
        NodeKind.STRIKETHROUGH: (u'\\sout{', u'}'),
        NodeKind.NEWLINE: u'\\\\\n',
    }

    def format(self, node):
        return self.auto_format(node)
