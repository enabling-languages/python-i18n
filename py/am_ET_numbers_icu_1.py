from icu import Locale, LocalizedNumberFormatter, Formattable, RuleBasedNumberFormat, URBNFRuleSetTag
lang = "am-ET-u-nu-ethi"
LOC = Locale.createCanonical(lang)
number = 123452
formatter = RuleBasedNumberFormat(URBNFRuleSetTag.SPELLOUT, LOC)

#
# Spellout (in Amharic)
# 
r = formatter.format(number)
print(r)
# መቶ ሁለት አስር ሦስት ሺ አራት መቶ አምስት አስር ሁለት

#
# Convert back
#
n = formatter.parse(r)
print(n)
# 123,452
print(Formattable.getInt64(n))
# 123452


