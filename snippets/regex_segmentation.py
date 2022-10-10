import regex
from el_internationalisation import cp


def regex_segmentation(text: str, pattern: str, sep: str = "\u200B", mode: list = ["list"]) -> list | str | None:
    """Tokenise string using regex, returning results as a list or string.

    Args:
        text (str): text to be segmented
        pattern (str): regex pattern for segmentation
        sep (str, optional): seperator to use if string is returned or results are displayed to STDOUT. Defaults to "\u200B" (ZWSP - Zero Width Space).
        display (bool, optional): Indicates whether results should displayed on STDOUT (True) or returned (False). Defaults to False.
        mode (str, optional): Indicates if results should be returned as a list or string, or displayed to STDOUT. Defaults to "list". Use "string" to return results as a string. Use "display" to output to STDOUT

    Returns:
        list | str | None: Results returned as list or string (see mode argument) or as None (if display)
    """
    result: str = regex.sub(pattern, r"\u200B\1", text)
    if result[0] == "\u200B":
        result = result[1:]
    result_list: list = result.split("\u200B")
    result_string: str = sep.join(result_list)
    if "display" in mode:
        print(
            f"Number of tokens: {str(len(result_list))} \nSegmentation boundaries: {result_string}")
    if "codepoints" in mode:
        for item in result_list:
            print(cp(item))
    if ("string" not in mode) and ("list" not in mode):
        print("Nothing to return")
        return None
    return result_string if "string" in mode else result_list

#####################
#
# Examples
#
#####################


s = 'ရန်ကုန်ကွန်ပျူတာတက္ကသိုလ်'
pattern = r'(?:(?<!္)([က-ဪဿ၊-၏]|[၀-၉]+|[^က-၏]+)(?![ှျ]?[့္်]))'
SEP = "\u2009·\u2009"

# Returns list
#
# Output:
#   ['ရန်', 'ကုန်', 'ကွန်', 'ပျူ', 'တာ', 'တက္က', 'သိုလ်']
l = regex_segmentation(s, pattern)
print(f"\n{l}\n")

# Print to STDOUT number of tokens, and segmentation boundary of
# token string using SEP
#
# Returns `None`
#
# Output to STDOUT:
#   Number of tokens: 7
#   Segmentation boundaries: ရန် · ကုန် · ကွန် · ပျူ · တာ · တက္က · သိုလ်
#   None
d = regex_segmentation(s, pattern, sep=SEP, mode=["display"])
print(d)
print("-----")

c = regex_segmentation(s, pattern, mode=["codepoints"])
print(c)
print("-----")

# Returns string with syllables seperated by pipe character
#
# Output
#   ရန်|ကုန်|ကွန်|ပျူ|တာ|တက္က|သိုလ်
sl = regex_segmentation(s, pattern, sep="|", mode=["string"])
print(sl)
print("-----")

# Returns string with syllbales seperated by ZWSP
#
# Output:
#   ရန်​ကုန်​ကွန်​ပျူ​တာ​တက္က​သိုလ်
sl2 = regex_segmentation(s, pattern, mode=["string"])
print(f"\n{sl2}")   # ရန်​ကုန်​ကွန်​ပျူ​တာ​တက္က​သိုလ်
print("-----")

lots = regex_segmentation(s, pattern, sep=SEP, mode=["codepoints", "list"])
print(lots)
print("-----")

lots2 = regex_segmentation(s, pattern, sep=SEP, mode=["display","codepoints", "string"])
print(lots2)
print("-----")

lots3 = regex_segmentation(s, pattern, sep=SEP, mode=["display","codepoints", "string"])
print(lots3)