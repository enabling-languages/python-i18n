#!/usr/bin/env python3

# #
# EL Util
#    various helper functions for internal Enabling Language projects
#
#    Copyright © 2021 Enabling Languages.
#    This file is made available under the MIT licence.
#

import os, sys
try:
    import unicodedataplus as ud
except ImportError:
    import unicodedata as ud
try:
    import regex as re
except ImportError:
    import re
import codecs
from tabulate import tabulate
import grapheme

# Code for interbnal testing and development:
#libpath = os.path.expanduser('~/dev/i18n/py/utils')
#if libpath not in sys.path:
#    sys.path.append(libpath)
#import cesu8

# Typecast string to a list, splitting characters
def splitString(text):
    return list(text)

def utf8len(text):
    return len(text.encode('utf-8'))

def utf16len(text):
    return len(text.encode('utf-16-le'))

# Replace values matching dictionary keys with values
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

# Normalise strings according to MARC21 Character repetoire requirements
# MNF (Marc Normalisation Form)
def marc21_normalise(text):
    # Normalise to NFD
    text = normalise(text, "NFD")
    # Latin variations between NFD and MNF
    latn_rep = {
    "\u004F\u031B": "Ơ",
    "\u008F\u031B": "ơ",
    "\u0055\u031B": "Ư",
    "\u0075\u031B": "ư"
    }
    # Cyrillic variations between NFD and MNF
    cyrl_rep = {
        "\u0418\u0306": "Й",
        "\u0438\u0306": "й",
        "\u0413\u0301": "Ѓ",
        "\u0433\u0301": "ѓ",
        "\u0415\u0308": "Ё",
        "\u0435\u0308": "ё",
        "\u0406\u0308": "Ї",
        "\u0456\u0308": "ї",
        "\u041A\u0301": "Ќ",
        "\u043A\u0301": "ќ",
        "\u0423\u0306": "Ў",
        "\u0443\u0306": "ў"
    }
    # Only process strings containing charcaters that need chasing
    if bool(re.search(r'[ouOU]\u031B', text)):
        text = replace_all(text, latn_rep)
    if bool(re.search(r'[\u0413\u041A\u0433\u043A]\u0301|[\u0418\u0423\u0438\u0443]\u0306|[\u0406\u0415\u0435\u0456]\u0308', text))
        text = replace_all(text, cyrl_rep)
    return text

# Normalise to specified Unicode Normalisation Form, defaulting to NFC.
# nf = NFC | NFKC | NFD | NFKD | MNF
def normalise(text, nf="NFC"):
    nf = nf.upper()
    if nf == "MNF":
        return marc21_normalise(text)
    if not (ud.is_normalized(nf, text)):
        return ud.normalize(nf, text)
    return text

# List of codepoints in string
def codepoints(text):
    return ' '.join('U+{:04X}'.format(ord(c)) for c in text)

# List codepoints and characters in string
def cp(text):
    return ' '.join(f"U+{ord(c):04X} ({c})" for c in text)

# table of codepoints in string, giving basic data on each charcater
def udata(text):
    print("String: " + text)
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

# Convert a string of comma or space seperated unicode codepoints to characters
#    Usage: codepointsToChar("U+0063 U+0301")
#        or codepointsToChar("0063 0301")
def codepointsToChar(str):
    str = str.lower().replace("u+", "")
    l = re.split(", |,| ", str)
    #l = str.lower().replace("u+", "").split(" ")
    r = ""
    for c in l:
        r += chr(int(c, 16))
    return r

# Get unicode codepoints for surrogate pairs for charcaters in SMP
#    Usage: surrogate_pair("𞤁")
def surrogatePair(c):
    if ord(c) > 0xffff:
        s1 = "".join(["{:02x}".format(x) for x in bytes(c, 'utf-16-le')[0:2]]).upper()
        s2 = "".join(["{:02x}".format(x) for x in bytes(c, 'utf-16-le')[2:4]]).upper()
        return "U+" + s1 + " U+" + s2
    return ""

# DEPRECATED: Use CESU-8 codec instead
def oracle_utf8(c):
    if ord(c) > 0xffff:
        s1 = "".join(["{:02x}".format(x) for x in bytes(c, 'utf-16-be')[0:2].decode('utf-16-be', 'surrogatepass').encode('utf-8', 'surrogatepass')]).upper()
        s2 = "".join(["{:02x}".format(x) for x in bytes(c, 'utf-16-be')[2:4].decode('utf-16-be', 'surrogatepass').encode('utf-8', 'surrogatepass')]).upper()
        return s1 + " " + s2
    return ""

# DEPRECATED: Use CESU-8 codec instead
def uni_bytes_oracle_utf8(c):
    if ord(c) > 0xffff:
        b1 = ["{:02x}".format(x) for x in bytes(c, 'utf-16-be')[0:2].decode('utf-16-be', 'surrogatepass').encode('utf-8', 'surrogatepass')]
        b2 = ["{:02x}".format(x) for x in bytes(c, 'utf-16-be')[2:4].decode('utf-16-be', 'surrogatepass').encode('utf-8', 'surrogatepass')]
        return b1 + b2
    return []


# Generate a table conatining byte sequences representing specified character in each Unicode encoding
#   Usage: byteSequences("𞤁")
def byteSequences(c, additional=[]):
    print("Character: " + c)
    print("Codepoint: " + "U+"+"%04X"%(ord(c)))
    if ord(c) > 0xffff:
        print("Surrogate pair: " + surrogatePair(c))
    data = [
        ['utf-8', " ".join(["{:02x}".format(x) for x in bytes(c, 'utf-8')]).upper()], 
        ['utf-16-le'," ".join(["{:02x}".format(x) for x in bytes(c, 'utf-16-le')]).upper()], 
        ['utf-16-be'," ".join(["{:02x}".format(x) for x in bytes(c, 'utf-16-be')]).upper()], 
        ['utf-32-le'," ".join(["{:02x}".format(x) for x in bytes(c, 'utf-32-le')]).upper()], 
        ['utf-32-be'," ".join(["{:02x}".format(x) for x in bytes(c, 'utf-32-be')]).upper()]
    ]
    #if additional.lower() == "cesu-8":
    if "cesu-8" in additional:
        data.append(['cesu-8', " ".join(["{:02x}".format(x) for x in codecs.encode(s, 'cesu-8')]).upper()] )
    datahead = ['Encoding', 'Byte sequence']
    print(tabulate(data, headers=datahead, tablefmt='grid'))

# Get list of unicode codepoints in a string
#    Usage: uni_cp("ꕙꔤ")
#           uni_cp("ꕙꔤ", False)
def uni_cp(txt, prefix=True):
    #return ["U+"+"%04X"%(ord(c)) for c in txt] if prefix else ["%04X"%(ord(c)) for c in txt]
    return ['U+{:04X}'.format(ord(c)) for c in txt] if prefix else ['{:04X}'.format(ord(c)) for c in txt]

# Get list of bytes that represent the string
#    Usage: uni_bytes("ꕙꔤ")
#           uni_bytes("ꕙꔤ", "utf-16-le")
def uni_bytes(txt, enc="utf-8"):
    enc = enc.lower()
    print(enc)
    #if mode.lower() =="oracle":
    #    return  uni_bytes_oracle_utf8(txt)
    if enc == "utf-8":
        return ["{:02x}".format(x) for x in bytes(txt, 'utf-8')]
    elif enc == "utf-16-le" or enc == "utf-16le":
        return ["{:02x}".format(x) for x in bytes(txt, 'utf-16-le')]
    elif enc == "utf-16-be" or enc == "utf-16be":
        return ["{:02x}".format(x) for x in bytes(txt, 'utf-16-be')]
    elif enc == "utf-32-le" or enc == "utf-32le":
        return ["{:02x}".format(x) for x in bytes(txt, 'utf-32-le')]
    elif enc == "utf-32-be" or enc == "utf-32be":
        return ["{:02x}".format(x) for x in bytes(txt, 'utf-32-be')]
    elif enc == "cesu-8":
        return ["{:02x}".format(x) for x in codecs.encode(txt, 'cesu-8')]
    return ""

# Force escaped surrogate pairs to be convert ro characters
#    Usage: surrogatesToChar("\u3AD8\u01DD")
def surrogatesToChar(seq):
    return seq.encode('utf-16', 'surrogatepass').decode('utf-16')


####################
#
#  TODO:
#
####################
#
#  1. strip bidi formating characters
#  2. strip punctuation
#  3. normalise white space, ie collapse multiple spaces to a single space, 
#     trim spaces at beginning of line or at end of line
#

def bidi_envelope(s, dir="auto", mode="isolate"):
    mode = mode.lower()
    dir = dir.lower()
    if mode == "isolate":
        if dir == "rtl":
            s = "\u2067" + s + "\u2069"
        elif dir == "ltr":
            s = "\u2066" + s + "\u2069"
        elif dir == "auto":
            s = "\u2068" + s + "\u2069"
    elif mode == "embedding":
        if dir == "auto":
            dir = "rtl"
        if dir == "rtl":
            s = "\u202B" + s + "\u202C"
        elif dir == "ltr":
            s = "\u202A" + s + "\u202C"
    return s


# strip bidi formating characters
def strip_bidi(s):
    # U+2066..U+2069, U+202A..U+202E
    return re.sub('[\u202a-\u202e\u2066-\u2069]', '', s)

# strip punctuation
def strip_punct(s, include=""):
    if include == "hyphen":
        #s = re.sub('\p{P}(?<!-)', '', s)
        #s = re.sub('\p{P}(?<!((\w-|-\w)))', '', s)
        s = re.sub('\p{P}(?<!(([^\b\s\p{P}]-)))', '', s)
        s = re.sub('-(?=[\s\b\p{P}])', '', s)
    elif include == "quote":
        #s = re.sub('\p{P}(?<!\')', '', s)
        #s = re.sub('\p{P}(?<!((\w\'|\'\w)))', '', s)
        s = re.sub('-(?=[\w])', ' ', s)
        s = re.sub('\p{P}(?<!(([^\b\s\p{P}]\')))', '', s)
        s = re.sub('\'(?=[\s\b\p{P}])', '', s)
    elif include == "both":
        #s = re.sub('\p{P}(?<![-\'])', '', s)
        #s = re.sub('\p{P}(?<!((\w[-\']|[-\']\w)))', '', s)
        s = re.sub('\p{P}(?<!(([^\b\s\p{P}][\'-])))', '', s)
        s = re.sub('[\'-](?=[\s\b\p{P}])', '', s)
    else:
        s = re.sub('-(?=[\w])', ' ', s)
        s = re.sub('\p{P}', '', s)
    return s
# test string 
#  \t\n  'Once upon'ga time, help; - trans-from here's 78 'the rub'?! 'Blah, blah' yeah.'    \t\n  
# 

def text_sanitise(s):
    s = ud.normalize("NFC", s)
    s = strip_bidi(s)
    s = strip_punct(s, include="both")
    s = s.strip()
    return s

# import el_utils as elu
# s = "𞤁𞤫𞤬𞤼𞤫𞤪𞤫 𞤨𞤢𞤴𞤳𞤮𞤴."
# print(elu.bidi_envelope(s, "rtl"))
# print(elu.strip_bidi(elu.bidi_envelope(s, "rtl")))

# macOS:
#    * Terminal - bidi support, but in LTR environment. Isolate and Ebedding modes work as epected.
#    * iTerm2 - no bidi support
#    * vsc integrated terminal - no bidi support



