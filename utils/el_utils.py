#!/usr/bin/env python3

# #
# EL Util
#    various helper functions for internal Enabling Language projects
#
#    Copyright © 2021-2022 Enabling Languages.
#    This file is made available under the MIT licence.
#
# Usage:
#    import os, sys
#    libpath = os.path.expanduser('~/dev/i18n/py/utils/')
#    if libpath not in sys.path:
#        sys.path.append(libpath)
#    import el_transliteration
#    import el_utils as elu

import os, sys, locale
import unicodedataplus as ud
import regex as re
import codecs
from tabulate import tabulate
import grapheme
from laonlp.tokenize import word_tokenize as lao_wt
from pythainlp.tokenize import word_tokenize as thai_wt
#from khmernltk import word_tokenize as khmer_wt
from icu import BreakIterator, Locale, UnicodeString, Transliterator, UTransDirection
# Code for interbnal testing and development:
# libpath = os.path.expanduser('~/dev/i18n/libr/yale-lao')
libpath = os.path.expanduser('./')
if libpath not in sys.path:
    sys.path.append(libpath)
#import cesu8
#from el_transliteration import transliteration_data
locale.setlocale(locale.LC_ALL, "")

ROOT_LOCALE = Locale.getRoot()
# DEFAULT_LOCALE = Locale("en-AU.UTF8")
DEFAULT_LOCALE = ROOT_LOCALE

# Typecast string to a list, splitting characters
def splitString(text):
    return list(text)

def utf8len(text):
    return len(text.encode('utf-8'))

def utf16len(text):
    return len(text.encode('utf-16-le'))

# Replace values matching dictionary keys with values
def replace_all(text, pattern_dict):
    for key in pattern_dict.keys():
        text = text.replace(key, str(pattern_dict[key]))
    return text

# Normalise to specified Unicode Normalisation Form, defaulting to NFC.
# nf = NFC | NFKC | NFD | NFKD | NFM
# NFM: Normalise strings according to MARC21 Character repetoire requirements
# TODO:
#    * Add support for NFKC_CF
def normalise(nf, text):
    nf = nf.upper()
    if nf not in ["NFC", "NFKC", "NFD", "NFKD", "NFM"]:
        nf="NFC"
    # MNF (Marc Normalisation Form)
    def marc21_normalise(text):
        # Normalise to NFD
        text = ud.normalize("NFD", text)
        # Latin variations between NFD and MNF
        latn_rep = {
            "\u004F\u031B": "\u01A0",
            "\u006F\u031B": "\u01A1",
            "\u0055\u031B": "\u01AF",
            "\u0075\u031B": "\u01B0"
        }
        # Cyrillic variations between NFD and MNF
        cyrl_rep = {
            "\u0418\u0306": "\u0419",
            "\u0438\u0306": "\u0439",
            "\u0413\u0301": "\u0403",
            "\u0433\u0301": "\u0453",
            "\u0415\u0308": "\u0401",
            "\u0435\u0308": "\u0451",
            "\u0406\u0308": "\u0407",
            "\u0456\u0308": "\u0457",
            "\u041A\u0301": "\u040C",
            "\u043A\u0301": "\u045C",
            "\u0423\u0306": "\u040E",
            "\u0443\u0306": "\u045E"
        }
        # Arabic variations between NFD and MNF
        arab_rep = {
            "\u0627\u0653": "\u0622",
            "\u0627\u0654": "\u0623",
            "\u0648\u0654": "\u0624",
            "\u0627\u0655": "\u0625",
            "\u064A\u0654": "\u0626"
        }
        # Only process strings containing characters that need replacing
        if bool(re.search(r'[ouOU]\u031B', text)):
            text = replace_all(text, latn_rep)
        if bool(re.search(r'[\u0413\u041A\u0433\u043A]\u0301|[\u0418\u0423\u0438\u0443]\u0306|[\u0406\u0415\u0435\u0456]\u0308', text)):
            text = replace_all(text, cyrl_rep)
        if bool(re.search(r'[\u0627\u0648\u064A]\u0654|\u0627\u0655|\u0627\u0653', text)):
            text = replace_all(text, arab_rep)
        return text
    if nf == "NFM":
        return marc21_normalise(text)
    return ud.normalize(nf, text)

# codepoints in string
# def codepoints(text, prefix=True):
#     return ' '.join('U+{:04X}'.format(ord(c)) for c in text) if prefix else ' '.join('{:04X}'.format(ord(c)) for c in text)

# codepoints and characters in string
#
# Usage:
#    elu.codepoints("𞤀𞤣𞤤𞤢𞤥 𞤆𞤵𞤤𞤢𞤪")
#    elu.cp("𞤀𞤣𞤤𞤢𞤥 𞤆𞤵𞤤𞤢𞤪", extended=False)
#    elu.cp("𞤀𞤣𞤤𞤢𞤥 𞤆𞤵𞤤𞤢𞤪", prefix=False, extended=False)

def codepoints(text, prefix=True, extended=True):
    if extended:
        return ' '.join(f"U+{ord(c):04X} ({c})" for c in text) if prefix else ' '.join(f"{ord(c):04X} ({c})" for c in text)
    else:
        return ' '.join('U+{:04X}'.format(ord(c)) for c in text) if prefix else ' '.join('{:04X}'.format(ord(c)) for c in text)

cp = codepoints

def graphemes(text):
    return re.findall(r'\X',text)

gr = graphemes

# Prepend dotted circle to combining diacritics in a string
# Input string, returns string
def add_dotted_circle(text):
    return "".join(["\u25CC" + i if ud.combining(i) else i for i in list(text)])

def isalpha_(text):
    if len(text) == 1:
        result = bool(re.match(r'[\p{Alphabetic}\p{Mn}\p{Mc}·]', text))
    else:
        result = bool(re.match(r'^\p{Alphabetic}[\p{Alphabetic}\p{Mn}\p{Mc}·]*$', text))
    # Add Mn and Mc categories to Unicode Alphabetic derived property
    # https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp
    return result

def isalpha_unicode(text):
    # Unicode Alphabetic derived property
    return bool(re.match(r'^\p{Alphabetic}+$', text))

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

# Get unicode codepoints for surrogate pairs for characters in SMP and SIP
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
        data.append(['cesu-8', " ".join(["{:02x}".format(x) for x in codecs.encode(c, 'cesu-8')]).upper()] )
    datahead = ['Encoding', 'Byte sequence']
    print(tabulate(data, headers=datahead, tablefmt='grid'))
    return

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
#  Bidi
#
####################
#  TODO:
#  1. strip bidi formating characters
#  2. strip punctuation
#  3. normalise white space, ie collapse multiple spaces to a single space, 
#     trim spaces at beginning of line or at end of line
#

def is_bidi(s):
    bidi_reg = r'[\p{bc=AL}\p{bc=AN}\p{bc=LRE}\p{bc=RLE}\p{bc=LRO}\p{bc=RLO}\p{bc=PDF}\p{bc=FSI}\p{bc=RLI}\p{bc=LRI}\p{bc=PDI}\p{bc=R}]'
    return bool(re.search(bidi_reg, s))

isbidi = is_bidi

# Wrap string in bidirection formatting characters
#    dir = ltr, rtl or auto
#    mode = isolate, embedding, override
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
    elif mode == "override":
        if dir == "auto":
            dir = "rtl"
        if dir == "rtl":
            s = "\u202E" + s + "\u202C"
        elif dir == "ltr":
            s = "\u202D" + s + "\u202C"
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

####################
#
#  Bibliographic data
#
####################
#  TODO:
#  1. add additional segmentation engines ofr Thai, Khmer, Myanmar and Tibetan
#  2. refactor transliteration
#     a. making a reversible transliteration wrapper
#     b. define rules for ALA-LC romanisation tables
#     b. add additional language dictionaries
#

#
# Word segmentation
#

# SUPPORTED_LANGUAGES = ['bo', 'bo_CN', 'bo_IN', 'km', 'km_KH', 'lo', 'lo_LA', 'my', 'my_MM', 'th', 'th_TH']
SUPPORTED_LANGUAGES = list(BreakIterator.getAvailableLocales())
SUPPORTED_ENGINES = ['icu', 'laonlp', 'thainlp']
SUPPORTED_SEPERATORS = ['\u0020', '\u007C', '\u200B']
SUPPORTED_NORMALISATION_FORMS = ['nfc', 'nfkc', 'nfd', 'nfkd', 'nfm']

def laonlp_tokenise(s, sep):
    s = sep.join(lao_wt(s))
    s = re.sub(r"\s{2,}", " ", s)
    return re.sub(r'\s([?.!"](?:\s|$))', r'\1', s)

#def thainlp_tokenise(s, sep):
#    s = sep.join(thai_wt(s))
#    s = re.sub(r"\s{2,}", " ", s)
#    return re.sub(r'\s([?.!"](?:\s|$))', r'\1', s)

def iterate_breaks(text, bi):
    bi.setText(text)
    lastpos = 0
    while True:
        next_boundary = bi.nextBoundary()
        if next_boundary == -1: return
        yield text[lastpos:next_boundary]
        lastpos = next_boundary

def icu_tokenise(s, l, sep):
    if l.lower() == "lo":
        bi = BreakIterator.createWordInstance(Locale('lo_LA'))
    if l.lower() == "th":
        bi = BreakIterator.createWordInstance(Locale('th_TH'))
    s = sep.join(list(iterate_breaks(s, bi)))
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r'\s([?.!"](?:\s|$))', r'\1', s)
    return s

def segment_words(text, engine="icu", lang="", sep="\u0020"):
    engine = engine.lower()
    lang = lang.replace("-", "_").split('.')[0]
    if engine not in SUPPORTED_ENGINES:
        print("Unsupported tokenisation engine specified", file=sys.stderr)
        sys.exit(1)
    if lang not in SUPPORTED_LANGUAGES:
        print("Unsupported language specified", file=sys.stderr)
        sys.exit(1)
    if sep not in SUPPORTED_SEPERATORS:
        print("Unsupported token seperator", file=sys.stderr)
        sys.exit(1)
    if engine == "icu":
        # return icu_tokenise(text, lang, sep)
        bi = BreakIterator.createWordInstance(Locale(lang))
        text = sep.join(list(iterate_breaks(text, bi)))
        text = re.sub(r"\s{2,}", " ", text)
        text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
        return text
    if engine == "laonlp" and lang[0:2] == "lo":
        return laonlp_tokenise(text, sep)
    # if engine == "thainlp" and lang[0:2] == "th":
    #     return thainlp_tokenise(text, sep)

#
# Transliteration
#

DEFAULT_NF = "NFD"

def prep_string(s, dir, lang, b="latin-only"):
    if dir.lower() == "reverse" and b.lower() != "both":
        s = s.lower()
    #s = ud.normalize('NFD', s)
    s = normalise(DEFAULT_NF, s)
    if lang == "lo" and dir.lower() == "reverse":
        s = s.replace("\u0327", "\u0328").replace("\u031C", "\u0328")
    return s

# direction (dir) = direction of transliteration ; forward (to Latin) | reverse (from Latin) 
# bicameral script (bicameral) = latin_only | both
# def to_native(bib_data, translit_table="laoo_t_latn_m0_ALALOC", dir="reverse", bicameral="latin_only" ):
#     bib_data = prep_string(bib_data, dir, bicameral)
#     word_dict = {}
#     if translit_table == "laoo_t_latn_m0_ALALOC":
#         from laoo_t_latn_m0_ALALOC import translit_dict, translit_rules
#         word_dict = translit_dict[dir]
#         label = "Lao-Latin/ALALOC"
#         #custom_transliterator = Transliterator.createFromRules(label, translit_rules, UTransDirection.REVERSE)
#         #res = " ".join(word_dict.get(ele, ele) for ele in bib_data.split())
#         bib_data_split = re.split('(\W+?)', bib_data)
#         res = "".join(word_dict.get(ele, ele) for ele in bib_data_split)
#         translit_result = res
#         #translit_result = custom_transliterator.transliterate(res)
#     else:
#         translit_result = bib_data
#     return translit_result

SUPPORTED_TRANSLITERATORS = {
    "bo": ("", "latin_only", ""),
    "kh": ("", "latin_only", ""),
    "lo": ("laoo_t_latn_m0_ALALOC", "latin_only", "Lao-Latin/ALALOC"),
    "my": ("", "latin_only", ""),
    "th": ("", "latin_only", "")
}

def el_transliterate(bib_data, lang, dir="forward", nf="nfd"):
    lang = lang.replace("-", "_").split('_')[0]
    dir = dir.lower()
    if dir != "reverse":
        dir = "forward"
    if SUPPORTED_TRANSLITERATORS[lang]:
        #bib_data = prep_string(bib_data, dir, SUPPORTED_TRANSLITERATORS[lang][1])
        translit_table = SUPPORTED_TRANSLITERATORS[lang]
        nf = nf.lower() if nf.lower() in SUPPORTED_NORMALISATION_FORMS else "nfd"
        bib_data = prep_string(bib_data, dir, lang, translit_table[1])
        word_dict = transliteration_data[translit_table[0]]['translit_dict'][dir]
        label = translit_table[2]
        if dir == "reverse":
            bib_data_split = re.split('(\W+?)', bib_data)
            res = "".join(word_dict.get(ele, ele) for ele in bib_data_split)
        else:
            pattern = re.compile('|'.join(word_dict.keys()))
            res = pattern.sub(lambda x: word_dict[x.group()], bib_data)
            # for key, value in word_dict.items():
            #    res = bib_data.replace(key, value)
            # bib_data_split = re.split('(\W+?)', bib_data)
            # res = "".join(word_dict.get(ele, ele) for ele in bib_data_split)
            # for key, value in word_dict.items():
            #     if key in bib_data:
            #         res = bib_data.replace(key, value)
    
    else:
        res = bib_data
    if nf != "nfd":
        res = normalise(nf, res)
    return res

# el_transliterate("vœ̄nvīlāvong", "lo-LA", dir="reverse")

# el_transliterate("vœ̄nvīlāvong", "lo", dir="reverse")

# el_transliterate("vœ̄nvīlāvong", "lo", dir="reverse", nf="nfd")

# test = "laoo_t_latn_m0_ALALOC"
# dir = "forward"
# rules_data = transliteration_data[test]['translit_dict'][dir]
# print(rules_data)
# ruleset = transliteration_data[test]["translit_rules"]
# print(ruleset)

#
# Numbers
#
#     * For chinese numbers: pycnnum 1.0.1  - https://pypi.org/project/pycnnum/
#     * Misc, including ethiopic https://github.com/jameshfisher/numeral
#     * https://blog.derso.org/recursive-algorithms-for-geez-numerals/
#          * https://github.com/ebenh/abyssinica/blob/52fa074b8fc0afad729513f56cda5c805212eae1/abyssinica/numerals.py#L124-#L149

# Convert decimal numbers to Arabic digits
#   s = string of digits
#   sep is a tuple containing the thousands (grouping) seperator and the decimal seperator
def convert_digits(s, sep = (",", ".")):
    nd = re.compile(r'^-?\p{Nd}[,.\u066B\u066C\u0020\u2009\u202F\p{Nd}]*$')
    tsep, dsep = sep
    if nd.match(s):
        s = s.replace(tsep, "")
        s = ''.join([str(ud.decimal(c, c)) for c in s])
        if dsep in s:
            s = float(s.replace(dsep, ".")) if dsep != "." else float(s)
            return s
        s = int(s.replace(dsep, ".")) if dsep != "." else  int(s)
    return s

# returns an int or float
#
# convert_digits('๓๒.๓')
# convert_digits("၉၃,၇၀၄.၈")
# convert_digits("၉၃,၇၀၄")
# convert_digits("1 234,01", (" ", ","))
# convert_digits('७,३७,७७,८८,६७३')

def is_number(v, sep = (",", ".")):
    original = v
    n = re.compile(r'^-?\p{N}[,.\u066B\u066C\u0020\u2009\u202F\p{N}]+$')
    nd = re.compile(r'^-?\p{Nd}[,.\u066B\u066C\u0020\u2009\u202F\p{Nd}]+$')
    v = "".join(v.split())
    if isinstance(v, int) or isinstance(v, float):
        return isinstance(v, (int, str)), type(v), v
    elif isinstance(v.strip(), str) and nd.match(v.strip()):
        v = convert_digits(v.strip(), sep)
        return True, type(v), v
    else:
        return False, type(v), v

# Returns tuple of boolean (is or isn't a decimal number), type, and value
# is_number('๓๒.๓')
# is_number("၉၃,၇၀၄.၈")
# is_number("၉၃,၇၀၄")
# is_number("1 234,01", (" ", ","))
# is_number('७,३७,७७,८८,६७३')


# https://unicode-org.github.io/cldr-staging/charts/latest/by_type/numbers.symbols.html#Symbols_using_Myanmar_Shan_Digits_(mymrshan)
# https://www.ezzeddinabdullah.com/posts/pythonic-translate
# https://stackoverflow.com/questions/20134737/python-matplotlib-use-locale-to-format-y-axis/20136623
# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale/numberingSystem
#
# convert_numeral_systems()
#
#    Convert numerals between numeral systems
#      * Default settings convert python int or float to the specified numeral system.
#      * Returns a string
#      * Two parameters added to assist in changing matplotlib tick labels: p and scale parameters.
#        These two parameters should be ignored in all other cases.

# import locale
def convert_numeral_systems(n, p=None, system_out="", system_in="latn", decimal=2, sep_in=["", "."], sep_out=["", "."], scale=None):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    decimal_places = decimal
    if system_in == "latn" and sep_in == ["", "."]:
        n = n / scale if scale else n
        format_string = '%0.' + str(decimal_places) + 'f' if type(n) == float else '%d'
        n = locale.format_string(format_string, n, grouping=True, monetary=True)
        n = n.replace(",", "ṯ").replace(".", "ḏ")
        #n = str(n)
    if sep_in[0] in [" ", ",", "٬", "\u2009"]:
        n = n.replace(r'[\u0020,٬\u2009]', "ṯ")
    elif sep_in[0] == ".":
        n = n.replace(".", "ṯ")
    if sep_in[1] in [",", ".", "٫"]:
        n = n.replace(r'[,.٫]', "ḏ")
    data = {
        "adlm" : {'name' : 'Adlam Digits (adlm)', "digits" : "𞥐𞥑𞥒𞥓𞥔𞥕𞥖𞥗𞥘𞥙", "sep_out": [",", "."]},
        "ahom" : {'name' : 'Ahom Digits (ahom)', "digits" : "𑜰𑜱𑜲𑜳𑜴𑜵𑜶𑜷𑜸𑜹"},
        "arab" : {'name' : 'Arabic-Indic Digits (arab)', "digits" : "٠١٢٣٤٥٦٧٨٩"},
        "arabext" : {'name' : 'Extended Arabic-Indic Digits (arabext)', "digits" : "۰۱۲۳۴۵۶۷۸۹", "sep_out_out": ["\u066C", "\u066B"]},
        "bali" : {'name' : 'Balinese Digits (bali)', "digits" : "᭐᭑᭒᭓᭔᭕᭖᭗᭘᭙"},
        "beng" : {'name' : 'Bangla Digits (beng)', "digits" : "০১২৩৪৫৬৭৮৯"},
        "bhks" : {'name' : 'Bhaiksuki  Digits (bhks)', "digits" : "𑱐𑱑𑱒𑱓𑱔𑱕𑱖𑱗𑱘𑱙"},
        "brah" : {'name' : 'Brahmi Digits (brah)', "digits" : "𑁦𑁧𑁨𑁩𑁪𑁫𑁬𑁭𑁮𑁯"},
        "cakm" : {'name' : 'Chakma Digits (cakm)', "digits" : "𑄶𑄷𑄸𑄹𑄺𑄻𑄼𑄽𑄾𑄿"},
        "cham" : {'name' : 'Cham Digits (cham)', "digits" : "꩐꩑꩒꩓꩔꩕꩖꩗꩘꩙"},
        "deva" : {'name' : 'Devanagari Digits (deva)', "digits" : "०१२३४५६७८९"},
        "diak" : {'name' : 'Dhives/Divehi Digits (diak)', "digits" : "𑥐𑥑𑥒𑥓𑥔𑥕𑥖𑥗𑥘𑥙"},
        "fullwide" : {'name' : 'Full-Width Digits (fullwide)', "digits" : "０１２３４５６７８９"},
        "gong" : {'name' : 'Gunjala Gondi digits (gong)', "digits" : "𑶠𑶡𑶢𑶣𑶤𑶥𑶦𑶧𑶨𑶩"},
        "gonm" : {'name' : 'Masaram Gondi digits (gonm)', "digits" : "𑵐𑵑𑵒𑵓𑵔𑵕𑵖𑵗𑵘𑵙"},
        "gujr" : {'name' : 'Gujarati Digits (gujr)', "digits" : "૦૧૨૩૪૫૬૭૮૯"},
        "guru" : {'name' : 'Gurmukhi Digits (guru)', "digits" : "੦੧੨੩੪੫੬੭੮੯"},
        "hmng" : {'name' : 'Pahawh Hmong Digits (hmng)', "digits" : "𖭐𖭑𖭒𖭓𖭔𖭕𖭖𖭗𖭘𖭙"},
        "hmnp" : {'name' : 'Nyiakeng Puachue Hmong Digits (hmnp)', "digits" : "𞅀𞅁𞅂𞅃𞅄𞅅𞅆𞅇𞅈𞅉"},
        "java" : {'name' : 'Javanese Digits (java)', "digits" : "꧐꧑꧒꧓꧔꧕꧖꧗꧘꧙"},
        "kali" : {'name' : 'Kayah Li Digits (kali)', "digits" : "꤀꤁꤂꤃꤄꤅꤆꤇꤈꤉"},
        "khmr" : {'name' : 'Khmer Digits (khmr)', "digits" : "០១២៣៤៥៦៧៨៩"},
        "knda" : {'name' : 'Kannada Digits (knda)', "digits" : "೦೧೨೩೪೫೬೭೮೯"},
        "lana" : {'name' : 'Tai Tham Hora Digits (lana)', "digits" : "᪀᪁᪂᪃᪄᪅᪆᪇᪈᪉"},
        "lanatham" : {'name' : 'Tai Tham Tham Digits (lanatham)', "digits" : "᪐᪑᪒᪓᪔᪕᪖᪗᪘᪙"},
        "laoo" : {'name' : 'Lao Digits (laoo)', "digits" : "໐໑໒໓໔໕໖໗໘໙"},
        "latn" : {'name' : 'Latin Digits (latn)', "digits" : "0123456789"},
        "lepc" : {'name' : 'Lepcha Digits (lepc)', "digits" : "᱀᱁᱂᱃᱄᱅᱆᱇᱈᱉"},
        "limb" : {'name' : 'Limbu Digits (limb)', "digits" : "᥆᥇᥈᥉᥊᥋᥌᥍᥎᥏"},
        "mlym" : {'name' : 'Malayalam Digits (mlym)', "digits" : "൦൧൨൩൪൫൬൭൮൯"},
        "modi" : {'name' : 'Modi Digits (modi)', "digits" : "𑙐𑙑𑙒𑙓𑙔𑙕𑙖𑙗𑙘𑙙"},
        "mong" : {'name' : 'Mongolian Digits (mong)', "digits" : "᠐᠑᠒᠓᠔᠕᠖᠗᠘᠙"},
        "mroo" : {'name' : 'Mro Digits (mroo)', "digits" : "𖩠𖩡𖩢𖩣𖩤𖩥𖩦𖩧𖩨𖩩"},
        "mtei" : {'name' : 'Meetei Mayek Digits (mtei)', "digits" : "꯰꯱꯲꯳꯴꯵꯶꯷꯸꯹"},
        "mymr" : {'name' : 'Myanmar Digits (mymr)', "digits" : "၀၁၂၃၄၅၆၇၈၉", "sep_out": [",", "."]},
        "mymrshan" : {'name' : 'Myanmar Shan Digits (mymrshan)', "digits" : "႐႑႒႓႔႕႖႗႘႙", "sep_out": [",", "."]},
        "mymrtlng" : {'name' : 'Myanmar Tai Laing Digits (mymrtlng)', "digits" : "꧰꧱꧲꧳꧴꧵꧶꧷꧸꧹"},
        "newa" : {'name' : 'Pracalit Digits (newa)', "digits" : "𑑐𑑑𑑒𑑓𑑔𑑕𑑖𑑗𑑘𑑙"},
        "nkoo" : {'name' : "N’Ko Digits (nkoo)", "digits" : "߀߁߂߃߄߅߆߇߈߉"},
        "olck" : {'name' : 'Ol Chiki Digits (olck)', "digits" : "᱐᱑᱒᱓᱔᱕᱖᱗᱘᱙"},
        "orya" : {'name' : 'Odia Digits (orya)', "digits" : "୦୧୨୩୪୫୬୭୮୯"},
        "osma" : {'name' : 'Osmanya Digits (osma)', "digits" : "𐒠𐒡𐒢𐒣𐒤𐒥𐒦𐒧𐒨𐒩"},
        "rohg" : {'name' : 'Hanifi Rohingya digits (rohg)', "digits" : "𐴰𐴱𐴲𐴳𐴴𐴵𐴶𐴷𐴸𐴹"},
        "saur" : {'name' : 'Saurashtra Digits (saur)', "digits" : "꣐꣑꣒꣓꣔꣕꣖꣗꣘꣙"},
        "shrd" : {'name' : 'Sharada Digits (shrd)', "digits" : "𑇐𑇑𑇒𑇓𑇔𑇕𑇖𑇗𑇘𑇙"},
        "sind" : {'name' : 'Khudabadi Digits (sind)', "digits" : "𑋰𑋱𑋲𑋳𑋴𑋵𑋶𑋷𑋸𑋹"},
        "sinh" : {'name' : 'Sinhala Digits (sinh)', "digits" : "෦෧෨෩෪෫෬෭෮෯"},
        "sora" : {'name' : 'Sora Sompeng Digits (sora)', "digits" : "𑃰𑃱𑃲𑃳𑃴𑃵𑃶𑃷𑃸𑃹"},
        "sund" : {'name' : 'Sundanese Digits (sund)', "digits" : "᮰᮱᮲᮳᮴᮵᮶᮷᮸᮹"},
        "takr" : {'name' : 'Takri Digits (takr)', "digits" : "𑛀𑛁𑛂𑛃𑛄𑛅𑛆𑛇𑛈𑛉"},
        "talu" : {'name' : 'New Tai Lue Digits (talu)', "digits" : "᧐᧑᧒᧓᧔᧕᧖᧗᧘᧙"},
        "tamldec" : {'name' : 'Tamil Digits (tamldec)', "digits" : "௦௧௨௩௪௫௬௭௮௯"},
        "tnsa" : {'name' : 'Tangsa Digits (tnsa)', "digits" : "𖫀𖫁𖫂𖫃𖫄𖫅𖫆𖫇𖫈𖫉"},
        "telu" : {'name' : 'Telugu Digits (telu)', "digits" : "౦౧౨౩౪౫౬౭౮౯"},
        "thai" : {'name' : 'Thai Digits (thai)', "digits" : "๐๑๒๓๔๕๖๗๘๙"},
        "tibt" : {'name' : 'Tibetan Digits (tibt)', "digits" : "༠༡༢༣༤༥༦༧༨༩"},
        "tirh" : {'name' : 'Tirhuta Digits (tirh)', "digits" : "𑓐𑓑𑓒𑓓𑓔𑓕𑓖𑓗𑓘𑓙"},
        "vaii" : {'name' : 'Vai Digits (vaii)', "digits" : "꘠꘡꘢꘣꘤꘥꘦꘧꘨꘩"},
        "wara" : {'name' : 'Warang Citi Digits (wara)', "digits" : "𑣠𑣡𑣢𑣣𑣤𑣥𑣦𑣧𑣨𑣩"},
        "wcho" : {'name' : 'Wancho Digits (wcho)', "digits" : "𞋰𞋱𞋲𞋳𞋴𞋵𞋶𞋷𞋸𞋹"}
        #"hanidec" : {'name' : 'Chinese Decimal Numerals (hanidec)', "digits": '', "sep_out": [",", "."]}
    }
    try:
        sep = data[system_out]['sep_out']
    except KeyError:
        sep = sep_out
    t = n.maketrans(data[system_in]["digits"], data[system_out]["digits"])
    locale.setlocale(locale.LC_ALL, "")
    return n.translate(t).replace("ṯ", sep[0] ).replace("ḏ", sep[1])



# ICU casing and casefolding
#   pass string, case (lower, upper, title, casefold), and icu.Locale object.
#   Return string either casefolded or converted to appropriate case.
def casing(text, case="lower", loc=None):
    if loc == None:
        loc = ROOT_LOCALE
    case = case.lower()
    if case == "lower":
        text = str(UnicodeString(text).toLower(loc))
    elif case == "upper":
        text = str(UnicodeString(text).toUpper(loc))
    elif case == "title":
        text = str(UnicodeString(text).toTitle(loc))
    elif case == "casefold" or case == "fold":
        text = str(UnicodeString(text).foldCase(loc))
    return text

#
# Casefolding and matching
# 

def caseless_match(x, y):
  return x.casefold() == y.casefold()

def canonical_caseless_match(x, y):
  return ud.normalize("NFD", ud.normalize("NFD", x).casefold()) == ud.normalize("NFD", ud.normalize("NFD", y).casefold())

def compatibility_caseless_match(x, y):
  return ud.normalize("NFKD", ud.normalize("NFKD", ud.normalize("NFD", x).casefold()).casefold()) == ud.normalize("NFKD", ud.normalize("NFKD", ud.normalize("NFD", y).casefold()).casefold())

def NFKC_Casefold(s):
  return ud.normalize("NFC", ud.normalize('NFKC', s).casefold())

def identifier_caseless_match(x, y):
  return NFKC_Casefold(ud.normalize("NFD", x)) == NFKC_Casefold(ud.normalize("NFD", y))

# Clean up presentation forms in data
#    Converts presentation forms to appropriate standard characters

def has_presentation_forms(text):
    pattern = r'([\p{InAlphabetic_Presentation_Forms}\p{InArabic_Presentation_Forms-A}\p{InArabic_Presentation_Forms-B}]+)'
    return bool(re.findall(pattern, text))

def clean_presentation_forms(text, folding=False):
    def clean_pf(match, folding):
        return  match.group(1).casefold() if folding else ud.normalize("NFKC", match.group(1))
    pattern = r'([\p{InAlphabetic_Presentation_Forms}\p{InArabic_Presentation_Forms-A}\p{InArabic_Presentation_Forms-B}]+)'
    return re.sub(pattern, lambda match, folding=folding: clean_pf(match, folding), text)


# Clean up doubled diacritics in data
#    Removes doubled diacrtics in data

def has_doubled_diacritics(text):
    return bool(re.findall(r'(\p{Mn})\1+', ud.normalize("NFD", text)))

def clean_diacritics(text, nf="nfc"):
    if not has_doubled_diacritics(text):
        return ud.normalize(nf.upper(), text)
    return ud.normalize(nf.upper(), re.sub(r'(\p{Mn})\1+', r'\1', ud.normalize("NFD", text)))

def data_check(text, nf="NFC"):
    print("Data check ...")
    if has_doubled_diacritics(text):
        print("* String has repeated contiguous diacritics.")
    if has_presentation_forms(text):
        print("* Presentation forms in string.")
    if bool(re.findall(r'\p{N}', text)) and bool(re.findall(r'[^0-9]', text)):
        print("* Non-Arabic numerals present in string")
    if ud.is_normalized("NFC", text) or ud.is_normalized("NFKC", text):
        print("* String uses precomposed characters")
    elif ud.is_normalized("NFD", text) or ud.is_normalized("NFKD", text):
        print("* String uses decomposed characters")
    print("Codepoints: ", codepoints(text))
    print("Unicode scripts: ", list(set([ud.script(a) for a in text])))





# add checks:
#    * RLO and LRO in string
#    * BOM at start of string
#    * check if data is precomposed (nfc, nfkc) or decomposed (nfd, nfkd)

# Test string
#     a = "Trá́ce, ﬁnd an oﬃce: ٣"
#     data_check(a)


