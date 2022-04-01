# import unicodedata as ud
# print(unicodedata.unidata_version)

# import unicodedata2 as unicodedata
# http://github.com/mikekap/unicodedata2
# https://pypi.org/project/unicodedata2/

try:
    import unicodedataplus as ud
except ImportError as e:
    print(e)
    print("Install unicodedataplus package")
# import unicodedataplus as unicodedata
# https://github.com/iwsfutcmd/unicodedataplus
# https://pypi.org/project/unicodedataplus/

import regex as re
# https://bitbucket.org/mrabarnett/mrab-regex
# https://pypi.org/project/regex/

try:
    import grapheme
except ImportError as e:
    print(e)
    print("Install grapheme package")
# https://github.com/alvinlindstam/grapheme
# https://pypi.org/project/grapheme/

# import tangled_up_in_unicode as ucd
# https://github.com/dylan-profiler/tangled-up-in-unicode
# https://pypi.org/project/tangled-up-in-unicode/

__ICUavailable__ = True
try:
    from icu import UnicodeString, Locale, Collator, RuleBasedCollator
except ImportError as e:
    __ICUavailable__ = False

from icu import *
# https://github.com/ovalhub/pyicu
# https://pypi.org/project/PyICU/

# from segments.tokenizer import Tokenizer
# https://github.com/cldf/segments
# https://github.com/unicode-cookbook/cookbook
# https://github.com/unicode-cookbook/recipes
# https://pypi.org/project/segments/
# https://github.com/cldf

# from pyuca import Collator
# https://github.com/jtauber/pyuca
try:
    from langcodes import *
except ImportError as e:
    print(e)
    print("Install langcodes package")
# https://github.com/LuminosoInsight/langcodes

try:
    from tabulate import tabulate
except ImportError as e:
    print(e)
    print('Install tabulate package')
# https://pypi.org/project/tabulate/


#################################################################
#
# Enabling Languages - Language enablement (el-le)
#
#     Language enablement python tools developed for Enabling Languages Open Source initiatives.
#     Released under the MIT license.
#
#     Copyright © 2020 Enabling Languages.
#
#################################################################
def splitString(s):
    return list(s)

def NFD(text):
    return ud.normalize('NFD', text)

def NFKD(text):
    return ud.normalize('NFKD', text)

def NFC(text):
    return ud.normalize('NFC', text)

def NFKC(text):
    return ud.normalize('NFKC', text)

# def is_normalised(unf, text):
#     unf = unf.upper()
#     return ud.normalize(unf, text) == text

def normalise(unf, text):
    unf = unf.upper()
    if not (ud.is_normalized(unf, text)):
        return ud.normalize(unf, text)
    return text


# Number of bytes in string:
#   See: https://stackoverflow.com/questions/30686701/python-get-size-of-string-in-bytes
def utf8len(s):
    return len(s.encode('utf-8'))

def utf16len(s):
    return len(s.encode('utf-16-le'))

# lengthData depreciated 
# def lengthData(s, nf="NFD"):
#     print("String: " + s)
#     print("Codepoints: " +  uu(s, unf=nf).codepoints())
#     print("\n")
#     data = [['Characters', len(s)], ['Bytes', utf8len(s)], ['Graphemes', grapheme.length(s)]]
#     datahead = ['Component', 'Count']
#     print(tabulate(data, headers=datahead, tablefmt='grid'))

collation_tailorings = {
    "din": "&A<<aa<<<aA<<<Aa<<<AA<<ä<<<Ä<<ää<<<äÄ<<<Ää<<<ÄÄ\n&D<dh<<<dH<<<Dh<<<DH\n&E<<ee<<<eE<<<Ee<<<EE<<ë<<<Ë<<ëë<<<ëË<<<Ëë<<<ËË<ɛ<<<Ɛ<<ɛɛ<<<ɛƐ<<<Ɛɛ<<<ƐƐ<<ɛ̈<<<Ɛ̈<<ɛ̈ɛ̈<<<ɛ̈Ɛ̈<<<Ɛ̈ɛ̈<<<Ɛ̈Ɛ̈\n&G<ɣ<<<Ɣ\n&I<<ii<<<iI<<<Ii<<<II<<ï<<<Ï<<ïï<<<ïÏ<<<Ïï<<<ÏÏ\n&N<nh<<<nH<<<Nh<<<NH<ny<<<nY<<<Ny<<<NH<ŋ<<<Ŋ\n&O<<oo<<<oO<<<Oo<<<OO<<ö<<<Ö<<öö<<<öÖ<<<Öö<<<ÖÖ<ɔ<<<Ɔ<<ɔɔ<<<ɔƆ<<<Ɔɔ<<<ƆƆ<<ɔ̈<<<Ɔ̈<<ɔ̈ɔ̈<<<ɔ̈Ɔ̈<<<Ɔ̈ɔ̈<<<Ɔ̈Ɔ̈\n&T<th<<<tH<<<Th<<<TH\n&U<<uu<<<uU<<<Uu<<<UU",
    "ak": "&E<ɛ<<<Ɛ\n&O<ɔ<<<Ɔ"
}


language_tailorings = {
    "din": "din",
    "din-SS": "din",
    "dip": "din",
    "dip-SS": "din",
    "diw": "din",
    "diw-SS": "din",
    "dib": "din",
    "dib-SS": "din",
    "dks": "din",
    "dks-SS": "din",
    "dik": "din",
    "dik-SS": "din",
    "ak":"ak",
    "ak-GH":"ak",
    "fat":"ak",
    "fat-GH":"ak",
    "bon":"ak",
    "bon-GH":"ak",
    "tw":"ak",
    "tw-GH":"ak"
}

class trk:
    def __init__(self, s, unf="NFD"):
        self.unf = unf.upper()
        self.s = normalise(self.unf, self.s)
    
    def __repr__(self):
        self.s = normalise(self.unf, self.s)
        return "<trk s:%s, unf:%s>" % (self.s, self.unf)

    def __str__(self):
        self.s = normalise(self.unf, self.s)
        return str(self.s)
    
    def lower_(self):
        self.s = normalise(self.unf, self.s)
        if (self.unf == "NFC" or self.unf == "NFKC"):
            self.s = self.s.replace('I', 'ı').replace('İ', 'i').lower()
        else:
            self.s = self.s.replace('I', 'ı').replace('I\u0307', 'i').lower()
        return self.s
    
    def casefold_(self):
        self.s = normalise(self.unf, self.s)
        if (self.unf == "NFC" or self.unf == "NFKC"):
            self.s = self.s.replace('I', 'ı').replace('İ', 'i').casefold()
        else:
            self.s = self.s.replace('I', 'ı').replace('I\u0307', 'i').lower()
        return self.s
    
    def upper_(self):
        self.s = normalise(self.unf, self.s)
        if (self.unf == "NFC" or self.unf == "NFKC"):
            self.s = self.s.replace('ı', 'I').replace('i', 'İ')
        else:
            self.s = self.s.replace('ı', 'I').replace('i', 'I\u0307')
        return self.s.upper()
    
    def capitalize_(self):
        self.s = normalise(self.unf, self.s)
        first, rest = self.s[0], self.s[1:]
        if (self.unf == "NFC" or self.unf == "NFKC"):
            t = first.replace('ı', 'I').replace('i', 'İ').upper() + rest.replace('I', 'ı').replace('İ', 'i').lower()
        else:
            t = first.replace('ı', 'I').replace('i', 'I\u0307').upper() + rest.replace('I', 'ı').replace('I\u0307', 'i').lower()
        return t
    
    def title_(self):
        self.s = normalise(self.unf, self.s)
        return " ".join(map(lambda x: trk(x).capitalize_(), self.s.split())) 

class ẞ:
    def __init__(self, s, unf="NFD"):
        self.unf = unf.upper()
        self.s = normalise(self.unf, self.s)
    
    def lower_(self):
        self.s = normalise(self.unf, self.s)
        return self.s.lower()
    
    def upper_(self):
        self.s = normalise(self.unf, self.s)
        self.s = self.s.replace('ß', 'ẞ')
        return self.s.upper()
    
    def capitalize_(self):
        self.s = normalise(self.unf, self.s)
        return self.s.capitalize()
    
    def title_(self):
        self.s = normalise(self.unf, self.s)
        return self.s.title()
    
    def casefold_(self):
        self.s = normalise(self.unf, self.s)
        ds = ""
        for i in range( len(self.s) ):
            if not (self.s[i] == "ẞ" or self.s[i] == "ß"):
                ds += self.s[i].casefold()
            else:
                ds += self.s[i].lower()
        return ds

class uCase:
    def __init__(self, s="", l="", forceẞ=False, unf="NFD"):
        # mode {'ẞ'}
        self.specCasingLanguages = ["az", "az-Latn", "tr", "nl", "lt"]
        self.unf = unf.upper()
        self.forceẞ = forceẞ
        defaultLang = "en-AU"
        #self.defaultLoc = Locale.forLanguageTag(defaultLang)
        if(l):
            self.l = l
            if (not l):
                l = defaultLang
            l = standardize_tag(l, macro=True)
            # loc = Locale.forLanguageTag(l)
            # if loc.getLanguage() in specCasingLanguages:
            #     self.loc = loc
            # else:
            #     self.loc = ""
            self.loc = Locale.forLanguageTag(l)
        else:
            self.l = ""
            self.loc = Locale.forLanguageTag(defaultLang)
        self.s = normalise(self.unf, self.s)
    
    def __repr__(self):
        self.s = normalise(self.unf, self.s)
        return "<uCase s:%s, l:%s, loc:%s, forceẞ:%s, unf:%s>" % (self.s, self.l, self.loc, self.forceẞ, self.unf)

    def __str__(self):
        self.s = normalise(self.unf, self.s)
        return str(self.s)

    def lower_(self):
        self.s = normalise(self.unf, self.s)
        if self.loc.getLanguage() in self.specCasingLanguages:
            self.s = str(UnicodeString(self.s).toLower(self.loc))
        else:
            self.s = self.s.lower()
        return self.s
    
    def upper_(self):
        self.s = normalise(self.unf, self.s)
        if (self.forceẞ):
            self.s = self.s.replace('ß', 'ẞ')
        if self.loc.getLanguage() in self.specCasingLanguages:
            self.s = str(UnicodeString(self.s).toUpper(self.loc))
        else:
            self.s = self.s.upper()
        return self.s
    
    def capitalize_(self):
        self.s = normalise(self.unf, self.s)
        if self.loc.getLanguage() in self.specCasingLanguages:
            if (self.loc.getLanguage() == "nl" and self.s[0:2].lower() == "ij"):
                self.s = str(UnicodeString(self.s[0:2]).toUpper(self.loc)) + str(UnicodeString(self.s[2:]).toLower(self.loc))
            else:
                self.s = str(UnicodeString(self.s[0]).toUpper(self.loc)) + str(UnicodeString(self.s[1:]).toLower(self.loc))
        else:
            self.s = self.s.capitalize()
        return self.s

    def title_(self):
        self.s = normalise(self.unf, self.s)
        if self.loc.getLanguage() in self.specCasingLanguages:
            self.s = str(UnicodeString(self.s).toTitle(self.loc))
        else:
             self.s = self.s.title()
        return self.s

    def casefold_(self):
        self.s = normalise(self.unf, self.s)
        if (self.forceẞ):
            ds = ""
            for i in range( len(self.s) ):
                if not (self.s[i] == "ẞ" or self.s[i] == "ß"):
                    ds += self.s[i].casefold()
                else:
                    ds += self.s[i].lower()
            self.s = ds
        if self.loc.getLanguage() in self.specCasingLanguages:
            if (self.loc.getLanguage() == "tr" or self.loc.getLanguage() == "az"):
                if (self.unf == "NFC" or self.unf == "NFKC"):
                    self.s = self.s.replace('I', 'ı').replace('İ', 'i').casefold()
                else:
                    self.s = self.s.replace('I', 'ı').replace('I\u0307', 'i').casefold()
            else:
                self.s = str(UnicodeString(self.s).foldCase())
        elif (not self.forceẞ):
            self.s = self.s.casefold()
        return self.s

class spCase:
    def __init__(self, s, mode, unf="NFD"):
        # mode {'ẞ', 'nl', 'lt'}
        self.unf = unf.upper()
        if(mode):
            self.mode = mode
        self.s = normalise(self.unf, self.s)
    
    def __repr__(self):
        self.s = normalise(self.unf, self.s)
        return "<spCase s:%s, mode:%s, unf:%s>" % (self.s, self.mode, self.unf)

    def __str__(self):
        self.s = normalise(self.unf, self.s)
        return str(self.s)

    def lower_(self):
        self.s = normalise(self.unf, self.s)
        return self.s.lower()
    
    def upper_(self):
        self.s = normalise(self.unf, self.s)
        if (self.mode == "ẞ"):
            self.s = self.s.replace('ß', 'ẞ')
        return self.s.upper()
    
    def capitalize_(self):
        self.s = normalise(self.unf, self.s)
        if (self.mode == "nl" and self.s[0:2].lower() == "ij"):
            self.s = self.s[0:2].upper() + self.s[2:].lower()
            return self.s
        return self.s.capitalize()
    
    # TODO:
    # title_() borken for IJ/ij in Dutch
    def title_(self):
        self.s = normalise(self.unf, self.s)
        if (self.mode == "nl"):
            #return " ".join(map(lambda x: spCase(x, self.unf, self.mode).capitalize_(), self.s.split()))
            l = self.s.split()
            nl = []
            for i in range(len(l)):
                nl.append(spCase(l[i], self.unf, self.mode).capitalize_())
            self.s = " ".join(nl)
        else:
            self.s = self.s.title()
        return self.s
    
    def casefold_(self):
        self.s = normalise(self.unf, self.s)
        if (self.mode == "ẞ"):
            ds = ""
            for i in range( len(self.s) ):
                if not (self.s[i] == "ẞ" or self.s[i] == "ß"):
                    ds += self.s[i].casefold()
                else:
                    ds += self.s[i].lower()
            self.s = ds
            return self.s
        else:
            return self.s.casefold()

class uu:
    def __init__(self, s="", l="", isTrk=False, unf="NFD", forceẞ=False, mode="script"):
        #self.s = s
        self.trk = isTrk
        self.unf = unf.upper()
        self.forceẞ = forceẞ
        self.l = l
        self.mode = mode
        self.s = normalise(self.unf, s)
        #if self.unf == "NFC":
        #    self.s = NFC(s)
        #elif self.unf == "NFKC":
        #    self.s = NFKC(s)
        #elif self.unf == "NFD":
        #    self.s = NFD(s)
        #else:
        #    self.s = NFKD(s)
    def __repr__(self):
        self.s = normalise(self.unf, self.s)
        return "<uu s:%s, l:%s, isTrk:%s, unf:%s, forceẞ:%s>" % (self.s, self.l, self.trk, self.unf, self.forceẞ)

    def __str__(self):
        self.s = normalise(self.unf, self.s)
        return str(self.s)

    def canonical_caseless(self):
        ICU = __ICUavailable__
        self.s = normalise(self.unf, self.s)
        if (self.trk):
            ICU = False
        if (ICU):
            if (self.unf == "NFD"):
                # canonical caseless
                # A string X is a canonical caseless match for a string Y if and only if:
                # NFD(toCasefold(NFD( X ))) = NFD(toCasefold(NFD( Y )))
                t = uCase(self.s, l=self.l, forceẞ=self.forceẞ, unf=self.unf)
                self.s = NFD(t.casefold_())
            elif (self.unf == "NFKC"):
                # identifier caseless
                # A string X is an identifier caseless match for a string Y if and only if:
                # toNFKC_Casefold(NFD( X)) = toNFKC_Casefold(NFD( Y ))
                t = uCase(s=self.s, l=self.l, forceẞ=self.forceẞ, unf=self.unf)
                self.s = t.casefold_()
            else:
                # compatibility caseless
                # A string X is a compatibility caseless match for a string Y if and only if:
                # NFKD(toCasefold(NFKD(toCasefold(NFD( X ))))) =NFKD(toCasefold(NFKD( ~~toCasefold(NFD( Y ))~~ )))
                t1 = uCase(self.s, l=self.l, forceẞ=self.forceẞ, unf="NFD")
                s = t1.casefold_()
                t2 = uCase(s, l=self.l, forceẞ=self.forceẞ, unf="NFKD")
                self.s = NFKD(t2)
        else:
            if (self.trk and self.unf == "NFD"):
                #self.s = NFD(NFD(trk(self.s, self.unf).casefold_()))
                return
            elif (self.trk and self.unf == "NFKD"):
                #self.s = ẞ(NFKD(NFKD(NFD(ẞ(s).casefold_())))).casefold_()
                return
            elif (self.trk and self.unf == "NFKC"):
                 return
            elif (self.forceẞ and self.unf == "NFD"):
                self.s = NFD(NFD(ẞ(self.s).casefold_()))
            elif (self.forceẞ and self.unf == "NFKD"):
                self.s = ẞ(NFKD(NFKD(NFD(ẞ(self.s).casefold_())))).casefold_()
            elif (self.forceẞ and self.unf == "NFKC"):
                self.s = ẞ(NFKC(self.s)).casefold_()
                # unicodedata.normalize('NFKC', s).casefold()
            elif (self.unf == "NFD"):
                self.s = NFD(NFD(self.s).casefold())
            elif (self.unf == "NFKC"):
                self.s = NFKC(self.s).casefold()
            else:
                self.s = NFKD(NFKD(NFD(self.s).casefold()).casefold())
        return self.s

    def codepoints(self):
        self.s = normalise(self.unf, self.s)
        if (self.mode == "console"):
            print(' '.join('U+{:04X}'.format(ord(c)) for c in self.s))
            return
        else:
            return ' '.join('U+{:04X}'.format(ord(c)) for c in self.s)
    
    def udata(self):
        self.s = normalise(self.unf, self.s)
        if (self.mode == "console"):
            print("  | cp | name | script | block | cat | bidi")
            for c in splitString(self.s):
                if ud.name(c,'-')!='-':
                    print(c,'|', "%04X"%(ord(c)), '|', ud.name(c,'-'), '|', ud.script(c), '|', ud.block(c), '|', ud.category(c), ' |',  ud.bidirectional(c))
            return
        else:
            message = "  | cp | name | script | block | cat | bidi\n"
            for c in splitString(self.s):
                if ud.name(c,'-')!='-':
                    message += c + '|' + "%04X"%(ord(c)) + '|' + ud.name(c,'-') + '|' + ud.script(c) + '|' + ud.block(c) + '|' + ud.category(c) + ' |' +  ud.bidirectional(c) + ' \n'
            return message
    
    def lengthData(self):
        self.s = normalise(self.unf, self.s)
        print("String: " + self.s)
        print("Codepoints: " +  uu(self.s, unf=self.unf).codepoints())
        #print("\n")
        data = [['Characters', len(self.s)], ['Bytes', utf8len(self.s)], ['Graphemes', grapheme.length(self.s)]]
        datahead = ['Component', 'Count']
        print(tabulate(data, headers=datahead, tablefmt='grid'))

# def is_caseless_match(x,y):
#     # toCasefold( X ) = toCasefold( Y )
#     # Need to rewrite to be language sensitive
#     return x.casefold() == y.casefold()

def is_canonical_caseless_match(x, y, lang="", nf="", forceẞ=""):
    # NFD(toCasefold(NFD( X ))) = NFD(toCasefold(NFD( Y ))
    tx = uCase(s=x, l=lang, unf="NFD", forceẞ=forceẞ)
    ty = uCase(s=y, l=lang, unf="NFD", forceẞ=forceẞ)
    return NFD(tx.casefold_()) == NFD(ty.casefold_())

def is_compatibility_caseless_match(x,y, lang="", forceẞ=""):
    # NFKD(toCasefold(NFKD(toCasefold(NFD( X ))))) = NFKD(toCasefold(NFKD(toCasefold(NFD( Y )))))
    tx = uCase(s=x, l=lang, unf="NFD", forceẞ=forceẞ)
    sx = tx.casefold_()
    tx.unf = "NFKD"
    tx.s = sx
    sx = tx.casefold_()
    ty = uCase(s=y, l=lang, unf="NFD", forceẞ=forceẞ)
    sy = ty.casefold_()
    ty.unf = "NFKD"
    ty.s = sy
    sy = ty.casefold_()
    return NFKD(sx) == NFKD(sy)

def is_identifier_caseless_match(x,y, lang="", nf="", forceẞ=""):
    # toNFKC_Casefold(NFD( X)) = toNFKC_Casefold(NFD( Y ))
    tx = uCase(s=x, l=lang, unf="NFKC", forceẞ=forceẞ)
    ty = uCase(s=y, l=lang, unf="NFKC", forceẞ=forceẞ)
    return tx.casefold_() == ty.casefold_()

# https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string


