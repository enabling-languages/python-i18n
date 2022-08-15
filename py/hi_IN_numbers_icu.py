from icu import Locale, LocalizedNumberFormatter, Formattable, RuleBasedNumberFormat, URBNFRuleSetTag
# lang = "hi-IN-u-nu-deva"
# lang = "en-IN"
lang = input("Enter language tag: ")
LOC = Locale.createCanonical(lang)

number = 123452.54
formatter = LocalizedNumberFormatter(LOC)
r = formatter.formatDouble(number)
print(r)
# १,२३,४५२.५४

rb_formatter = RuleBasedNumberFormat(URBNFRuleSetTag.SPELLOUT, LOC)
r2 = rb_formatter.format(number)
print(r2)
# एक लाख तेईस हज़ार चार सौ बावन दशमलव पाँच चार

r3 = rb_formatter.parse(r2)
print(Formattable.getDouble(r3))
# 123452.54

