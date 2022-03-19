####################
#
# Normalisation
#   © Enabling Languages 2022
#   Released under the MIT License.
#
####################

# import unicodedata as ud
import unicodedataplus as ud


def NFD(s):
    return ud.normalize('NFD', s)

def NFKD(s):
    return ud.normalize('NFKD', s)

def NFC(s):
    return ud.normalize('NFC', s)

def NFKC(s):
    return ud.normalize('NFKC', s)
