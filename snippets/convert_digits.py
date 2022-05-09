####################
#
# Convert digits
#   © Enabling Languages 2022
#   Released under the MIT License.
#
####################

import unicodedataplus as ud, regex as re
import locale

#
# To Western Arabic digits
#
def convert_digits(s, sep = (",", ".")):
    nd = re.compile(r'^-?\p{Nd}[,.\u066B\u066C\u0020\u2009\p{Nd}]*$')
    tsep, dsep = sep
    if nd.match(s):
        s = s.replace(tsep, "")
        s = ''.join([str(ud.decimal(c, c)) for c in s])
        if dsep in s:
            return float(s.replace(dsep, ".")) if dsep != "." else float(s)
        return int(s)
    return s

def is_number(v, sep = (",", ".")):
    original = v
    n = re.compile(r'^-?\p{N}[,.\u066B\u066C\u0020\u2009\p{N}]+$')
    nd = re.compile(r'^-?\p{Nd}[,.\u066B\u066C\u0020\u2009\p{Nd}]+$')
    v = "".join(v.split())
    if isinstance(v, int) or isinstance(v, float):
        return isinstance(v, (int, str)), type(v), v
    elif isinstance(v.strip(), str) and nd.match(v.strip()):
        v = convert_digits(v.strip(), sep)
        return True, type(v), v
    else:
        return False, type(v), v

#
# From Western Arabic digits
#
def convert_numerals(n, system="arabext", decimal=2, sep=["", "."]):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    decimal_places = decimal
    format_string = '%0.' + str(decimal_places) + 'f' if type(n) == float else '%d'
    n = locale.format_string(format_string, n, grouping=True, monetary=True)
    n = n.replace(",", "ṯ").replace(".", "ḏ")
    n = str(n)
    data = {
        "adlm" : {'name' : 'Adlam Digits (adlm)', "digits" : "𞥐𞥑𞥒𞥓𞥔𞥕𞥖𞥗𞥘𞥙", "sep": [",", "."]},
        "ahom" : {'name' : 'Ahom Digits (ahom)', "digits" : "𑜰𑜱𑜲𑜳𑜴𑜵𑜶𑜷𑜸𑜹"},
        "arab" : {'name' : 'Arabic-Indic Digits (arab)', "digits" : "٠١٢٣٤٥٦٧٨٩"},
        "arabext" : {'name' : 'Extended Arabic-Indic Digits (arabext)', "digits" : "۰۱۲۳۴۵۶۷۸۹", "sep": ["\u066C", "\u066B"]},
        "bali" : {'name' : 'Balinese Digits (bali)', "digits" : "᭐᭑᭒᭓᭔᭕᭖᭗᭘᭙"},
        "beng" : {'name' : 'Bangla Digits (beng)', "digits" : "০১২৩৪৫৬৭৮৯"},
        "bhks" : {'name' : 'Bhaiksuki  Digits (bhks)', "digits" : "𑱐𑱑𑱒𑱓𑱔𑱕𑱖𑱗𑱘𑱙"},
        "brah" : {'name' : 'Brahmi Digits (brah)', "digits" : "𑁦𑁧𑁨𑁩𑁪𑁫𑁬𑁭𑁮𑁯"},
        "cakm" : {'name' : 'Chakma Digits (cakm)', "digits" : "𑄶𑄷𑄸𑄹𑄺𑄻𑄼𑄽𑄾𑄿"},
        "cham" : {'name' : 'Cham Digits (cham)', "digits" : "꩐꩑꩒꩓꩔꩕꩖꩗꩘꩙"},
        "deva" : {'name' : 'Devanagari Digits (deva)', "digits" : "०१२३४५६७८९"},
        "diak" : {'name' : 'Dhives/Divehi Digits (diak)', "digits" : "𑥐𑥑𑥒𑥓𑥔𑥕𑥖𑥗𑥘𑥙"},
        "fullwide" : {'name' : 'Full-Width Digits (fullwide)', "digits" : "０１２３４５６７８９"},
        "gong" : {'name' : 'Gunjala Gondi digits (gong)', "digits" : "𑶠𑶡𑶢𑶣𑶤𑶥𑶦𑶧𑶨𑶩"},
        "gonm" : {'name' : 'Masaram Gondi digits (gonm)', "digits" : "𑵐𑵑𑵒𑵓𑵔𑵕𑵖𑵗𑵘𑵙"},
        "gujr" : {'name' : 'Gujarati Digits (gujr)', "digits" : "૦૧૨૩૪૫૬૭૮૯"},
        "guru" : {'name' : 'Gurmukhi Digits (guru)', "digits" : "੦੧੨੩੪੫੬੭੮੯"},
        "hmng" : {'name' : 'Pahawh Hmong Digits (hmng)', "digits" : "𖭐𖭑𖭒𖭓𖭔𖭕𖭖𖭗𖭘𖭙"},
        "hmnp" : {'name' : 'Nyiakeng Puachue Hmong Digits (hmnp)', "digits" : "𞅀𞅁𞅂𞅃𞅄𞅅𞅆𞅇𞅈𞅉"},
        "java" : {'name' : 'Javanese Digits (java)', "digits" : "꧐꧑꧒꧓꧔꧕꧖꧗꧘꧙"},
        "kali" : {'name' : 'Kayah Li Digits (kali)', "digits" : "꤀꤁꤂꤃꤄꤅꤆꤇꤈꤉"},
        "khmr" : {'name' : 'Khmer Digits (khmr)', "digits" : "០១២៣៤៥៦៧៨៩"},
        "knda" : {'name' : 'Kannada Digits (knda)', "digits" : "೦೧೨೩೪೫೬೭೮೯"},
        "lana" : {'name' : 'Tai Tham Hora Digits (lana)', "digits" : "᪀᪁᪂᪃᪄᪅᪆᪇᪈᪉"},
        "lanatham" : {'name' : 'Tai Tham Tham Digits (lanatham)', "digits" : "᪐᪑᪒᪓᪔᪕᪖᪗᪘᪙"},
        "laoo" : {'name' : 'Lao Digits (laoo)', "digits" : "໐໑໒໓໔໕໖໗໘໙"},
        "latn" : {'name' : 'Latin Digits (latn)', "digits" : "0123456789"},
        "lepc" : {'name' : 'Lepcha Digits (lepc)', "digits" : "᱀᱁᱂᱃᱄᱅᱆᱇᱈᱉"},
        "limb" : {'name' : 'Limbu Digits (limb)', "digits" : "᥆᥇᥈᥉᥊᥋᥌᥍᥎᥏"},
        "mlym" : {'name' : 'Malayalam Digits (mlym)', "digits" : "൦൧൨൩൪൫൬൭൮൯"},
        "modi" : {'name' : 'Modi Digits (modi)', "digits" : "𑙐𑙑𑙒𑙓𑙔𑙕𑙖𑙗𑙘𑙙"},
        "mong" : {'name' : 'Mongolian Digits (mong)', "digits" : "᠐᠑᠒᠓᠔᠕᠖᠗᠘᠙"},
        "mroo" : {'name' : 'Mro Digits (mroo)', "digits" : "𖩠𖩡𖩢𖩣𖩤𖩥𖩦𖩧𖩨𖩩"},
        "mtei" : {'name' : 'Meetei Mayek Digits (mtei)', "digits" : "꯰꯱꯲꯳꯴꯵꯶꯷꯸꯹"},
        "mymr" : {'name' : 'Myanmar Digits (mymr)', "digits" : "၀၁၂၃၄၅၆၇၈၉", "sep": [",", "."]},
        "mymrshan" : {'name' : 'Myanmar Shan Digits (mymrshan)', "digits" : "႐႑႒႓႔႕႖႗႘႙", "sep": [",", "."]},
        "mymrtlng" : {'name' : 'Myanmar Tai Laing Digits (mymrtlng)', "digits" : "꧰꧱꧲꧳꧴꧵꧶꧷꧸꧹"},
        "newa" : {'name' : 'Pracalit Digits (newa)', "digits" : "𑑐𑑑𑑒𑑓𑑔𑑕𑑖𑑗𑑘𑑙"},
        "nkoo" : {'name' : "N’Ko Digits (nkoo)", "digits" : "߀߁߂߃߄߅߆߇߈߉"},
        "olck" : {'name' : 'Ol Chiki Digits (olck)', "digits" : "᱐᱑᱒᱓᱔᱕᱖᱗᱘᱙"},
        "orya" : {'name' : 'Odia Digits (orya)', "digits" : "୦୧୨୩୪୫୬୭୮୯"},
        "osma" : {'name' : 'Osmanya Digits (osma)', "digits" : "𐒠𐒡𐒢𐒣𐒤𐒥𐒦𐒧𐒨𐒩"},
        "rohg" : {'name' : 'Hanifi Rohingya digits (rohg)', "digits" : "𐴰𐴱𐴲𐴳𐴴𐴵𐴶𐴷𐴸𐴹"},
        "saur" : {'name' : 'Saurashtra Digits (saur)', "digits" : "꣐꣑꣒꣓꣔꣕꣖꣗꣘꣙"},
        "shrd" : {'name' : 'Sharada Digits (shrd)', "digits" : "𑇐𑇑𑇒𑇓𑇔𑇕𑇖𑇗𑇘𑇙"},
        "sind" : {'name' : 'Khudabadi Digits (sind)', "digits" : "𑋰𑋱𑋲𑋳𑋴𑋵𑋶𑋷𑋸𑋹"},
        "sinh" : {'name' : 'Sinhala Digits (sinh)', "digits" : "෦෧෨෩෪෫෬෭෮෯"},
        "sora" : {'name' : 'Sora Sompeng Digits (sora)', "digits" : "𑃰𑃱𑃲𑃳𑃴𑃵𑃶𑃷𑃸𑃹"},
        "sund" : {'name' : 'Sundanese Digits (sund)', "digits" : "᮰᮱᮲᮳᮴᮵᮶᮷᮸᮹"},
        "takr" : {'name' : 'Takri Digits (takr)', "digits" : "𑛀𑛁𑛂𑛃𑛄𑛅𑛆𑛇𑛈𑛉"},
        "talu" : {'name' : 'New Tai Lue Digits (talu)', "digits" : "᧐᧑᧒᧓᧔᧕᧖᧗᧘᧙"},
        "tamldec" : {'name' : 'Tamil Digits (tamldec)', "digits" : "௦௧௨௩௪௫௬௭௮௯"},
        "tnsa" : {'name' : 'Tangsa Digits (tnsa)', "digits" : "𖫀𖫁𖫂𖫃𖫄𖫅𖫆𖫇𖫈𖫉"},
        "telu" : {'name' : 'Telugu Digits (telu)', "digits" : "౦౧౨౩౪౫౬౭౮౯"},
        "thai" : {'name' : 'Thai Digits (thai)', "digits" : "๐๑๒๓๔๕๖๗๘๙"},
        "tibt" : {'name' : 'Tibetan Digits (tibt)', "digits" : "༠༡༢༣༤༥༦༧༨༩"},
        "tirh" : {'name' : 'Tirhuta Digits (tirh)', "digits" : "𑓐𑓑𑓒𑓓𑓔𑓕𑓖𑓗𑓘𑓙"},
        "vaii" : {'name' : 'Vai Digits (vaii)', "digits" : "꘠꘡꘢꘣꘤꘥꘦꘧꘨꘩"},
        "wara" : {'name' : 'Warang Citi Digits (wara)', "digits" : "𑣠𑣡𑣢𑣣𑣤𑣥𑣦𑣧𑣨𑣩"},
        "wcho" : {'name' : 'Wancho Digits (wcho)', "digits" : "𞋰𞋱𞋲𞋳𞋴𞋵𞋶𞋷𞋸𞋹"}
        #"hanidec" : {'name' : 'Chinese Decimal Numerals (hanidec)', "digits": '', "sep": [",", "."]}
    }
    try:
        sep = data[system]['sep']
    except KeyError:
        sep = sep
    t = n.maketrans(data["latn"]["digits"], data[system]["digits"])
    locale.setlocale(locale.LC_ALL, "")
    return n.translate(t).replace("ṯ", sep[0] ).replace("ḏ", sep[1])


#
# Locale formatted numbers using PyICU
#   Supports both integers and floating point numbers.
#
from icu import Locale, NumberFormat

def icu_formatted_digits(d, loc=None):
    if loc is None:
        loc = Locale.getRoot()
    formatter = NumberFormat.createInstance(loc)
    return formatter.format(d)