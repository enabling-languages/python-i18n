import arabic_reshaper
from bidi.algorithm import get_display

from el_internationalisation import cp, clean_presentation_forms

def rtl_hack(text: str, arabic: bool = True) -> str:
    """Visually reorders Arabic or Hebrew script Unicode text

    Visually reorders Arabic or Hebrew script Unicode text. For Arabic script text,
    individual Unicode characters are substituting each character for its equivalent
    presentation form. The modules are used to overcome lack of bidirectional algorithm
    and complex font rendering in some modules and terminals.

    It is better to solutions that utilise proper bidirectional algorithm and font
    rendering implementations. For matplotlib use the mplcairo backend instead. For
    annotating images use Pillow. Both make use of libraqm.

    arabic_reshaper module converts Arabic characters to Arabic Presentation Forms:
        pip install arabic-reshaper

    bidi.algorithm module converts a logically ordered string to visually ordered
    equivalent.
        pip install python-bidi

    Args:
        text (str): _description_

    Returns:
        str: _description_
    """
    return get_display(arabic_reshaper.reshape(text)) if arabic == True else get_display(text)

text = 'اللغة العربية رائعة'
text_h = rtl_hack(text)
print(text)
print(cp(text))
print(text_h)
print(cp(text_h))





s1 = "لا"
s1_h = rtl_hack(s1)
s2 = "لأ"
s2_h = rtl_hack(s2)

print("\n")
print(s1)
print(cp(s1))
print(s1_h)
print(cp(s1_h))

print("\n")
print(s2)
print(cp(s2))
print(s2_h)
print(cp(s2_h))


s3 = "עברית חדשה"
s3_h = rtl_hack(s3, arabic=False)
print("\n")
print(s3)
print(cp(s3))
print(s3_h)
print(cp(s3_h))
# print(s3_h == s3[::-1])


# Note s3[::-1] is used for reversing strings,
# but for languages that use combining marks,
# it is better to reverse grapheme clusters:
#
#   from grapheme import graphemes
#   print(s3_h == "".join(list(graphemes(s3))[::-1]))

from grapheme import graphemes
def reverse_string(text: str, use_graphemes: bool = False) -> str:
    return "".join(list(graphemes(text))[::-1]) if use_graphemes else text[::-1]

import regex as re
def reverse_string_regex(text: str, use_graphemes: bool = False) -> str:
    return "".join(re.findall(r'\X', text)[::-1]) if use_graphemes else text[::-1]

print("---")
# print(s3_h == "".join(list(graphemes(s3))[::-1]))
# print("\n")
print(text_h == text[::-1])
print(clean_presentation_forms(text_h) == text[::-1])
# print(clean_presentation_forms(text_h) == "".join(list(graphemes(text))[::-1]))


print(clean_presentation_forms(text_h) == reverse_string(text))
print(clean_presentation_forms(text_h) == reverse_string(text, use_graphemes=True))

print(clean_presentation_forms(text_h) == reverse_string_regex(text))
print(clean_presentation_forms(text_h) == reverse_string_regex(text, use_graphemes=True))