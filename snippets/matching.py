####################
#
# Unicode matching
#
#   © Enabling Languages 2022
#   Released under the MIT License.
#
####################

import unicodedataplus as ud

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
