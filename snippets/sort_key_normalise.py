####################
#
# normalised_sort
#
#   © Enabling Languages 2022
#   Released under the MIT License.
#
#   Normalise text before sorting. This key finction will perform Unicode normalisation and
#   will lowercase the strings before sorting.
#
#   Usage:
#     * sorted(my_list, key=normalised_sort)  OR  my_list.sort(key=normalised_sort)
#     * sorted(my_list, key=lambda x: normalised_sort(x, "NFD"))  OR  my_list.sort(key=lambda x: normalised_sort(x, "NFD"))
#
####################

import unicodedata as ud

def normalised_sort(s, nf="NFC"):
    if nf.upper() in ["NFC", "NFKC", "NFD", "NFKD"]:
        return ud.normalize(nf, s).lower()
    return s
