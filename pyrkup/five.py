#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement, division, absolute_import, print_function


import sys


# five - because 2 + 3 is better than 2 * 3 :)
PY2 = sys.version_info[0] == 2
if not PY2:
    binary_type = bytes
    text_type = str
    string_types = (str,)
    unichr = chr
else:
    binary_type = str
    text_type = unicode
    string_types = (str, unicode)
    unichr = unichr


def force_unicode(text):
    if isinstance(text, binary_type):
        return text.decode('utf-8')
    else:
        return text_type(text)
