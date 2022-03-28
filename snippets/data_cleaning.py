####################
#
# Data cleaning
#   © Enabling Languages 2022
#   Released under the MIT License.
#
####################

# import unicodedata as ud
import unicodedataplus as ud
import regex as re
from icu import UnicodeString, Locale, Normalizer2, UNormalizationMode2


#
# Unicode normalisation
#   Simple wrappers for Unicode normalisation
#

def NFD(s, engine=ud):
    if engine == "icu":
        normalizer = Normalizer2.getInstance(None, "nfc", UNormalizationMode2.DECOMPOSE)
        return normalizer.normalize(s)
    return ud.normalize('NFD', s)

def NFKD(s, engine=ud):
    if engine == "icu":
        normalizer = Normalizer2.getInstance(None, "nfkc", UNormalizationMode2.DECOMPOSE)
        return normalizer.normalize(s)
    return ud.normalize('NFKD', s)

def NFC(s, engine=ud):
    if engine == "icu":
        normalizer = Normalizer2.getInstance(None, "nfc", UNormalizationMode2.COMPOSE)
        return normalizer.normalize(s)
    return ud.normalize('NFC', s)

def NFKC(s, engine=ud):
    if engine == "icu":
        normalizer = Normalizer2.getInstance(None, "nfkc", UNormalizationMode2.COMPOSE)
        return normalizer.normalize(s)
    return ud.normalize('NFKC', s)

#
# Clean presentation forms
#
#    For Latin and Armenian scripts, use either folding=True or folding=False (default), 
#    while for Arabic and Hebrew scripts, use folding=False.
#

def has_presentation_forms(text):
    pattern = r'([\p{InAlphabetic_Presentation_Forms}\p{InArabic_Presentation_Forms-A}\p{InArabic_Presentation_Forms-B}]+)'
    return bool(re.findall(pattern, text))

def clean_presentation_forms(text, folding=False):
    def clean_pf(match, folding):
        return  match.group(1).casefold() if folding else ud.normalize("NFKC", match.group(1))
    pattern = r'([\p{InAlphabetic_Presentation_Forms}\p{InArabic_Presentation_Forms-A}\p{InArabic_Presentation_Forms-B}]+)'
    return re.sub(pattern, lambda match, folding=folding: clean_pf(match, folding), text)

# PyICU Helper functions for casing and casefolding.
# s is a string, l is an ICU locale object (defaulting to CLDR Root Locale)
def toLower(s, l=Locale.getRoot()):
    return str(UnicodeString(s).toLower(l))
def toUpper(s, l=Locale.getRoot()):
    return str(UnicodeString(s).toUpper(l))
def toTitle(s, l=Locale.getRoot()):
    return str(UnicodeString(s).toTitle(l))
def toSentence(s, l=Locale.getRoot()):
    return(str(UnicodeString(s[0]).toUpper(l)) + str(UnicodeString(s[1:]).toLower(l)))
def foldCase(s):
    return str(UnicodeString(s).foldCase())

#
# Turkish casing implemented without module dependencies.
# PyICU provides a more comprehensive solution for Turkish.
#

# To lowercase
def kucukharfyap(s):
    return ud.normalize("NFC", s).replace('İ', 'i').replace('I', 'ı').lower()

# To uppercase
def buyukharfyap(s):
    return ud.normalize("NFC", s).replace('ı', 'I').replace('i', 'İ').upper()
