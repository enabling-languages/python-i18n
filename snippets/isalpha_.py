####################
#
# isalpha_()
#
#   © Enabling Languages 2022
#   Released under the MIT License.
#
####################

import regex as re

# Add Mn and Mc categories and interpunct to Unicode Alphabetic derived property
def isalpha_(text):
    if len(text) == 1:
        result = bool(re.match(r'[\p{Alphabetic}\p{Mn}\p{Mc}·]', text))
    else:
        result = bool(re.match(r'^\p{Alphabetic}[\p{Alphabetic}\p{Mn}\p{Mc}·]*$', text))
    return result

# Unicode Alphabetic derived property
def isalpha_unicode(text):
    return bool(re.match(r'^\p{Alphabetic}+$', text))
