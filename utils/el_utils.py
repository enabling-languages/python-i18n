#
# EL Util
#    various helper functions
#
#    Copyright © 2021 Enabling Languages.
#    This notebook is made available under the MIT licence.
#

import unicodedataplus as ud
from tabulate import tabulate
import grapheme

# Typecast string to a list, splitting characters
def splitString(text):
    return list(text)

def utf8len(text):
    return len(text.encode('utf-8'))

def utf16len(text):
    return len(text.encode('utf-16-le'))

# Normalise to specified Unicode Normalisation Form, defaulting to NFC.
def normalise(text, nf="NFC"):
    nf = nf.upper()
    if not (ud.is_normalized(nf, text)):
        return ud.normalize(nf, text)
    return text

# List of codepoints in string
def codepoints(text):
    return ' '.join('U+{:04X}'.format(ord(c)) for c in text)

# table of codepoints in string, giving basic data on each charcater
def udata(text):
    data = []
    datahead = ["char", "cp", "name", "script", "block", "cat", "bidi"]
    for c in splitString(text):
        if ud.name(c,'-')!='-':
            data.append([c, "%04X"%(ord(c)), ud.name(c,'-'), ud.script(c), ud.block(c), ud.category(c), ud.bidirectional(c)])
    print(tabulate(data, headers=datahead, tablefmt='grid'))

def stringLength(text):
    print("String: " + text)
    print("Codepoints: " +  codepoints(text))
    data = [
        ['Characters', len(text)], 
        ['Bytes', utf8len(text)], 
        ['Graphemes', grapheme.length(text)],
        ['Syllables', ""], 
        ['Words', ""]
    ]
    datahead = ['Component', 'Count']
    print(tabulate(data, headers=datahead, tablefmt='grid'))