####################
#
# Data cleaning
#   © Enabling Languages 2022
#   Released under the MIT License.
#
####################

import unicodedataplus as ud
import regex as re

def convert_digits(s, sep = (",", ".")):
    nd = re.compile(r'^-?\p{Nd}[,.\u066B\u066C\u0020\u2009\p{Nd}]+$')
    tsep, dsep = sep
    if nd.match(s):
        s = s.replace(tsep, "")
        s = ''.join([str(ud.decimal(c, c)) for c in s])
        if dsep in s:
            s = float(s.replace(dsep, ".")) if dsep != "." else float(s)
            return s
        s = int(s.replace(dsep, ".")) if dsep != "." else  int(s)
    return s
