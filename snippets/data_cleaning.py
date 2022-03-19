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


#
# Unicode normalisation
#   Simple wrappers for Unicode normalisation
#


def NFD(s):
    return ud.normalize('NFD', s)

def NFKD(s):
    return ud.normalize('NFKD', s)

def NFC(s):
    return ud.normalize('NFC', s)

def NFKC(s):
    return ud.normalize('NFKC', s)



#
# Clean presentation forms
#
#    For Latin and Armenian scripts, use either folding=True or folding=False (default), while 
#    for Arabic and Hebrew scripts, use folding=False.
#    

def has_presentation_forms(text):
    pattern = r'([\p{InAlphabetic_Presentation_Forms}\p{InArabic_Presentation_Forms-A}\p{InArabic_Presentation_Forms-B}]+)'
    return bool(re.findall(pattern, text))

def clean_presentation_forms(text, folding=False):
    def clean_pf(match, folding):
        return  match.group(1).casefold() if folding else ud.normalize("NFKC", match.group(1))
    pattern = r'([\p{InAlphabetic_Presentation_Forms}\p{InArabic_Presentation_Forms-A}\p{InArabic_Presentation_Forms-B}]+)'
    return re.sub(pattern, lambda match, folding=folding: clean_pf(match, folding), text)
