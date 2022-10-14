###############################
#
# Collation _rules
#
###############################

# Akan (ak, fat, twi, wss)
ak_rules = fat_rules = twi_rules = wss_rules = (
    "&E<ɛ<<<Ɛ"
    "&O<ɔ<<<Ɔ"
)

# Dinka (din, dip, diw, dib, dks, dik)
din_rules = dip_rules = diw_rules = dib_rules = dks_rules = dik_rules = (
    "[normalization on]"
    "&A<<aa<<<Aa<<<AA<<ä<<<Ä<<ää<<<Ää<<<ÄÄ"
    "&D<dh<<<Dh<<<DH"
    "&E<<ee<<<Ee<<<EE<<ë<<<Ë<<ëë<<<Ëë<<<ËË<ɛ<<<Ɛ<<ɛɛ<<<Ɛɛ<<<ƐƐ<<ɛ̈<<<Ɛ̈<<ɛ̈ɛ̈<<<Ɛ̈ɛ̈<<<Ɛ̈Ɛ̈"
    "&G<ɣ<<<Ɣ"
    "&I<<ii<<<II<<ï<<<Ï<<ïï<<<Ïï<<<ÏÏ"
    "&N<nh<<<Nh<<<NH<ny<<<Ny<<<NY<ŋ<<<Ŋ"
    "&O<<oo<<<Oo<<<OO<<ö<<<Ö<<öö<<<Öö<<<ÖÖ<ɔ<<<Ɔ<<ɔɔ<<<Ɔɔ<<<ƆƆ<<ɔ̈<<<Ɔ̈<<ɔ̈ɔ̈<<<Ɔ̈ɔ̈<<<Ɔ̈Ɔ̈"
    "&T<th<<<Th<<<TH"
    "&U<<uu<<<UU"
)

# Shan (shn, shn-Mymr, shn-Mymr-MM)   from sldr
shn_rules = (
    "&ၵ < ၶ < ၷ < င < ၸ < သ < ၺ < ၹ < တ < ၻ < ၼ < ပ < ၽ < ၾ < ၿ < မ < ယ < ရ < လ < ဝ < ႀ < ႁ"
    "&ႁ < ႃ < ိ < ီ < ော် < ေ < ၤ < ု < ူ < ုဝ် < ူဝ် < ေႃ် < ေႃ < ိုဝ် < ိူဝ် < ႆ < ၺ်"
    "&ၺ် < ၢႆ < ၢၺ် < ူၺ် < ွႆ < ွၺ် < ိုၺ် < ိူၺ် < ႟ < ဝ်"
    "&ဝ် < ၢဝ် < ိဝ် < ဵဝ် < ႅဝ် < ိုဝ်ဝ် < ိူဝ်ဝ် < ွ် < ၵ်"
    "&ၵ် < ၢၵ် < ိၵ် < ဵၵ် < ႅၵ် < ုၵ် < ူၵ် < ွၵ် < ိုၵ် < ိူၵ် < ၵ်ျ"
    "&ၵ်ျ < ၢၵ်ျ < ိၵ်ျ < ဵၵ်ျ < ႅၵ်ျ < ုၵ်ျ < ူၵ်ျ < ွၵ်ျ < ိုၵ်ျ < ိူၵ်ျ < ၶ်"
    "&ၶ် < ၢၶ် < ိၶ် < ဵၶ် < ႅၶ် < ုၶ် < ူၶ် < ွၶ် < ိုၶ် < ိူၶ် < ၶ်ျ"
    "&ၶ်ျ < ၢၶ်ျ < ိၶ်ျ < ဵၶ်ျ < ႅၶ်ျ < ုၶ်ျ < ူၶ်ျ < ွၶ်ျ < ိုၶ်ျ < ိူၶ်ျ < ၷ်"
    "&ၷ် < ၢၷ် < ိၷ် < ဵၷ် < ႅၷ် < ုၷ် < ူၷ် < ွၷ် < ိုၷ် < ိူၷ် < ၷ်ျ"
    "&ၷ်ျ < ၢၷ်ျ < ိၷ်ျ < ဵၷ်ျ < ႅၷ်ျ < ုၷ်ျ < ူၷ်ျ < ွၷ်ျ < ိုၷ်ျ < ိူၷ်ျ < င်"
    "&င် < ၢင် < ိင် < ဵင် < ႅင် < ုင် < ူင် < ွင် < ိုင် < ိူင် < ၸ်"
    "&ၸ် < ၢၸ် < ိၸ် < ဵၸ် < ႅၸ် < ုၸ် < ူၸ် < ွၸ် < ိုၸ် < ိူၸ် < သ်"
    "&သ် < ၢသ် < ိသ် < ဵသ် < ႅသ် < ုသ် < ူသ် < ွသ် < ိုသ် < ိူသ် < သ်ျ"
    "&သ်ျ < ၢသ်ျ < ိသ်ျ < ဵသ်ျ < ႅသ်ျ < ုသ်ျ < ူသ်ျ < ွသ်ျ < ိုသ်ျ < ိူသ်ျ < ၹ်"
    "&ၹ် < ၢၹ် < ိၹ် < ဵၹ် < ႅၹ် < ုၹ် < ူၹ် < ွၹ် < ိုၹ် < ိူၹ် < တ်"
    "&တ် < ၢတ် < ိတ် < ဵတ် < ႅတ် < ုတ် < ူတ် < ွတ် < ိုတ် < ိူတ် < ၻ်"
    "&ၻ် < ၢၻ် < ိၻ် < ဵၻ် < ႅၻ် < ုၻ် < ူၻ် < ွၻ် < ိုၻ် < ိူၻ် < ၼ်"
    "&ၼ် < ၢၼ် < ိၼ် < ဵၼ် < ႅၼ် < ုၼ် < ူၼ် < ွၼ် < ိုၼ် < ိူၼ် < ပ်"
    "&ပ် < ၢပ် < ိပ် < ဵပ် < ႅပ် < ုပ် < ူပ် < ွပ် < ိုပ် < ိူပ် < ၽ်"
    "&ၽ် < ၢၽ် < ိၽ် < ဵၽ် < ႅၽ် < ုၽ် < ူၽ် < ွၽ် < ိုၽ် < ိူၽ် < ၾ်"
    "&ၾ် < ၢၾ် < ိၾ် < ဵၾ် < ႅၾ် < ုၾ် < ူၾ် < ွၾ် < ိုၾ် < ိူၾ် < ၿ်"
    "&ၿ် < ၢၿ် < ိၿ် < ဵၿ် < ႅၿ် < ုၿ် < ူၿ် < ွၿ် < ိုၿ် < ိူၿ် < မ်"
    "&မ် < ၢမ် < ိမ် < ဵမ် < ႅမ် < ုမ် < ူမ် < ွမ် < ိုမ် < ိူမ် < ယ်"
    "&ယ် < ၢယ် < ိယ် < ဵယ် < ႅယ် < ုယ် < ူယ် < ွယ် < ိုယ် < ိူယ် < ရ်"
    "&ရ် < ၢရ် < ိရ် < ဵရ် < ႅရ် < ုရ် < ူရ် < ွရ် < ိုရ် < ိူရ် < လ်"
    "&လ် < ၢလ် < ိလ် < ဵလ် < ႅလ် < ုလ် < ူလ် < ွလ် < ိုလ် < ိူလ် < ႀ်"
    "&ႀ် < ၢႀ် < ိႀ် < ဵႀ် < ႅႀ် < ုႀ် < ူႀ် < ွႀ် < ိုႀ် < ိူႀ် < ႁ်"
    "&ႁ် < ၢႁ် < ိႁ် < ဵႁ် < ႅႁ် < ုႁ် < ူႁ် < ွႁ် < ိုႁ် < ိူႁ် < ျ < ြ < ႂ"
    "&[last secondary ignorable] <<ႇ <<ႈ <<း <<ႉ <<ႊ"
    "&ိၼ် < ိၺ်"
    "&မ် < ံ"
    "&ၢမ် < ၢံ"
    "&ိမ် < ်ံ"
    "&ုမ် < ုံ"
    "&ူမ် < ူံ"
    "&ွမ် < ွံ"
)

# Sgaw Karen (ksw)    from UTN11 v4
ksw_rules = (
    "&\u1021 < \u1027"
    "< \u1062\u103A < \u102C\u103A < \u1038 < \u1063\u103A < \u1064"
    "< \u102B < \u1036 < \u1062 < \u102F < \u1030 < \u1037 < \u1032 < \u102D < \u102E"
    "< \u103E < \u1060 < \u103B < \u103C < \u103D"
    "&\u1012 < \u1012\u103A / \u1036"
    "&\u1019 < \u1019\u103A / \u102E\u1064"
)

# Kayah (kyu-Mymr)   from UTN11 v4
kyu_Mymr_rules = (
    "&\u1021 < \u1064 < \u1038"
    "< \u1072 < \u102E < \u102D < \u1036 < \u1032 < \u1073 < \u1074 < \u1034"
    "< \u102F < \u1030 < \u103C < \u103B < \u103D < \u103E"
)

# Sorani Kurdish (Iraq) ckb_IQ  Using glibc  https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=localedata/locales/ckb_IQ;hb=HEAD
ckb_glibc_rules = ckb_IQ_glibc_rules = (
    "[normalization on]"
    "[reorder Arab]"
    "&\u0631<\u0695"
    "&\u0646<\u0648<\u06C6"
)

# Sorani Kurdish (Iraq) ckb_IQ  Using sort order of the Kurdish Academy standard 
ckb_rules = ckb_IQ_rules = (
    "[normalization on]"
    "[reorder Arab]"
    "&\u0631 < \u0695 < \u0632"
    "&\u0648 < \u06C6 < \u0648\u0648"
)