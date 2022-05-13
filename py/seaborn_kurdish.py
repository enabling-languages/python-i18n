#
# seaborn_kurdish.py
#
#   This script will read in and process a Sorani Kurdish TSV file.
#   Two plots will be generated (a LTR layout and a RTL layout).
#   
#   mplcairo supports a number of backends available. 
#
#   If you wish to save plot as an image, rather than display plot
#   use module://mplcairo.base
#
#   Depending on your OS and system configuration a number of 
#   backends that render to widgets are available:
#      * module://mplcairo.gtk (used below for non-macOS installs)
#      * module://mplcairo.gtk_native
#      * module://mplcairo.qt
#      * module://mplcairo.tk
#      * module://mplcairo.wx
#      * module://mplcairo.macosx  (used below for macOS)

import pandas as pd
import locale, platform
import gi
import mplcairo
import matplotlib as mpl
if platform.system() == "Darwin":
    mpl.use("module://mplcairo.macosx")
else:
    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")
    # mpl.use("module://mplcairo.qt")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import unicodedata as ud, regex as re

# Convert non-Western Arabic digits to Western Arabic digits
def convert_digits(s, sep = (",", ".")):
    nd = re.compile(r'^-?\p{Nd}[,.\u066B\u066C\u0020\u2009\u202F\p{Nd}]*$')
    tsep, dsep = sep
    if nd.match(s):
        s = s.replace(tsep, "")
        s = ''.join([str(ud.decimal(c, c)) for c in s])
        if dsep in s:
            return float(s.replace(dsep, ".")) if dsep != "." else float(s)
        return int(s)
    return s

# Specify grouping and decimal seperators using in data
seps = ("\u066C", "\u066B")
# convert entries to hyphen to Eastern Arabic zero, and pass to convert_digits()
digitsconv = lambda x: convert_digits(x.replace("-", "٠"), sep = seps)

# Covert Western Arabic digits to Eastern Arabic digits for tick labels
def convert_to_sorani_ns(n, p=None, scale=None):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    decimal_places = 2
    n = n * scale if scale else n
    format_string = '%0.' + str(decimal_places) + 'f' if type(n) == float else '%d'
    n = locale.format_string(format_string, n, grouping=True, monetary=True)
    n = n.replace(",", "ṯ").replace(".", "ḏ")
    sep = ["\u066C", "\u066B"]
    t = n.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    locale.setlocale(locale.LC_ALL, "")
    return n.translate(t).replace("ṯ", sep[0] ).replace("ḏ", sep[1])

# import data
import pandas as pd
conv = {
    'سووریا': digitsconv,
    'عێراق': digitsconv,
    'ئێران': digitsconv,
    'تورکیا': digitsconv,
    'جیھانی': digitsconv
}
df = pd.read_table("../data/demographics.tsv", converters=conv)
print(df)

# get sum of each column
col_list=["تورکیا" ,"ئێران" ,"عێراق" ,"سووریا"]
total_df = df[col_list].sum(axis=0)
print(total_df)

# Plot data. First subplot (axes[0]) is default layout, second subplot (axes[1]) is an RTL layout
sns.set_style('darkgrid')
sns.set_context({"font.family": "Vazirmatn"})
fig, axes = plt.subplots(1,2)
sns.barplot(x=total_df.index, y=total_df.values, ax=axes[0])
sns.barplot(x=total_df.index, y=total_df.values, ax=axes[1])

# set common labels for X and Y axes.
plt.setp(axes, xlabel="ناوچە")
plt.setp(axes, ylabel="ڕێژەی دانیشتووان (بە ملیۆن)")
# Set single title for all subplots
fig.suptitle('ڕێژەی دانیشتووانی کورد')

# Define and apply conversion to tick labels for both axes
ns_formatter = ticker.FuncFormatter(lambda x, p: convert_to_sorani_ns(x, p, scale=0.000001))
axes[0].get_yaxis().set_major_formatter(ns_formatter)
axes[1].get_yaxis().set_major_formatter(ns_formatter)

# move y axis and associated label to right of axes[1]
axes[1].yaxis.tick_right()
axes[1].yaxis.set_label_position("right")
# invert x-axis for axes[1]
#plt.gca().invert_xaxis()
axes[1].invert_xaxis()

# block=True required for running script in CLI when outputting canvas to widget.
plt.show(block=True)