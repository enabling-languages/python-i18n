import pyuca
test_list = ["₨", "Z", "ز", "z", "ر", "٨", "R", "﷼"]
ducet_rules = "../rules/collation/allkeys_DUCET.txt"
cldr_rules = "../rules/collation/allkeys_CLDR.txt"
ducet_collator = pyuca.Collator(ducet_rules)
cldr_collator = pyuca.Collator(cldr_rules)

sorted_default = sorted(test_list)
print(sorted_default)
sorted_ducet = sorted(test_list, key=ducet_collator.sort_key)
print(sorted_ducet)
sorted_cldr = sorted(test_list, key=cldr_collator.sort_key)
print(sorted_cldr)

from icu import Locale, Collator
loc = Locale.getRoot()
collator = Collator.createInstance(loc)
sorted_icu_root = sorted(test_list, key=collator.getSortKey)
print(sorted_icu_root)

print(sorted_icu_root == sorted_cldr)