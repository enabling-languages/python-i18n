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
#   nf (normalisation form): {NFC, NFKC, NFD, NFKD}
#   loc (use locale): {True, False}
#
#   Usage:
#     * sorted(my_list, key=normalised_sort)  OR  my_list.sort(key=normalised_sort)
#     * sorted(my_list, key=lambda x: normalised_sort(x, "NFD"))  OR  my_list.sort(key=lambda x: normalised_sort(x, "NFD"))
#     * sorted(my_list, key=lambda x: normalised_sort(x, "NFC", loc=True))  OR  my_list.sort(key=lambda x: normalised_sort(x, "NFC", loc=True))
#
#  For examples see gist: https://gist.github.com/andjc/821d85f0e10549f9e4ab8c84c1ee00f5
#
# ####################

import locale
import unicodedata as ud

def normalised_sort(s, nf="NFD", loc=False):
    nf = nf.upper()
    if nf in ["NFC", "NFKC", "NFD", "NFKD"]:
        s = locale.strxfrm(ud.normalize(nf, s.lower())) if loc else ud.normalize(nf, s.lower())
    return s

# Function to assist in locale specific or ICU sorting
def df_sort(series, key):
    def sort_series(key=None,reverse=False):
        def sorter(series):
            series_list = list(series)
            return [series_list.index(i) for i in sorted(series_list,key=key,reverse=reverse)]
        return sorter
    if (isinstance(series, pd.Series)):
        sort_by_custom_dict = sort_series(key=key)
        return df.iloc[sort_by_custom_dict(series)]
