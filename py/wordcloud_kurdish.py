import gi, platform, os
import mplcairo
import matplotlib as mpl
if platform.system() == "Darwin":
    mpl.use("module://mplcairo.macosx")
else:
    gi.require_version("Gtk", "3.0")
    mpl.use("module://mplcairo.gtk")
    # mpl.use("module://mplcairo.qt")
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Stopword list from klpt (Kurdish Language Processing Toolkit)
# Available stopword lists: Sorani (Arabic) and Kurmanji (Latin)
def get_kurdish_stopwords(dialect, script):
    from urllib.request import urlopen
    import json
    url = "https://raw.githubusercontent.com/sinaahmadi/klpt/master/klpt/data/stopwords.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    return set(data_json[dialect][script])

ckb_stopwords = get_kurdish_stopwords("Sorani", "Arabic")
text = """
زمانی کوردی
لە ئینسایکڵۆپیدیای ئازادی ویکیپیدیاوە
ئەم وتارە سەبارەت بە زمانی کوردی نووسراوە. بۆ شاعیرە کوردەکە، بڕوانە کوردی (شاعیر). بۆ وتارە ھاوشێوەکان، بڕوانە کوردی (ڕوونکردنەوە).
زمانی کوردی (بە کرمانجی، بە سۆرانی: زمانی کوردی، بە کەڵهوڕی: زوان کوردی، بە لەکی: زوۆن کوردی، بە زازاکی، بە ھەورامی: زوانو کوردی) زمانێکە کە خەڵکی کورد قسەی پێدەکەن. لە ڕووی بنەماڵەوە بەشێکە لە زمانە ھیندوئەورووپایییەکان. ئەم زمانە لە زمانی کەڤناری مادی کەوتووەتەوە. زمانی کوردی لە نێوان زمانە ئێرانییەکاندا لە بواری پرژماربوونی ئاخێوەران سێیەمین زمانە و دەکەوێتە دوای زمانەکانی فارسی و پەشتۆ.
شێوەزارەکانی کوردی
وتاری سەرەکی: شێوەزارەکانی زمانی کوردی
زمانی کوردی چەند شێوەزارێکی سەرەکی ھەیە کە جیاوازیی زۆریان ھەیە و زمانناسەکان لە سەر چۆنیەتی جیاکردنەوەی ئەم شێوەزارانە یەکدەنگ نین و زۆرێک لە زمانناسەکان باوەڕییان بە ماڵباتی زمانگەلی کوردی ھەیە. یانی کورمانجیی باکووری و گۆرانی، بە پێی یاسا و ڕێسای زمانناسی و زمانەوانییەوە، دو زمانی سەربەخۆی کوردینە، نەک دو شێوەزار. بەڵام زۆربەی ئەو کەسانەی زمانی(زمانەکانی) کوردییان دابەش کردووە، بەم چوار دەستەیە بووە
    کوردیی باکووری
    کوردیی ناوەندی
    کوردیی باشووری
    گۆرانی-زازایی
ھەندێک لە زمانناسان، لوڕیش وەک شێوەزارێکی زمانی کوردی پۆلبەند دەکەن. ئەگەر چی لوڕی ژمارەیەکی زۆری وشەی کوردی تێدایە، بەڵام ھێشتاش لێکۆلینەوەیەکی ئەوتۆ لە سەر لوڕی لە بەر دەستدا نییە.
ئەلفوبێی کوردی
وتار سەرەکییەکان: ئەلفوبێکانی کوردی و ئەلفوبێی عەرەبیی زمانی کوردی
بەھۆی ئەوەی کە کوردەکان لە ژێر دەسەڵاتی عوسمانی و ئێران بوون و ئەلفوبێی فەرمیی ئەو دوو وڵاتە ئەلفوبێی عەرەبی بوو، کوردەکانیش تا پێش سییەکان تەنیا ئەلفوبێی عەرەبییان بۆ نووسینی کوردی بەکار دەھێنا. لە تورکیا، لە دوای بە فەرمیکردنی ئەلفوبێی لاتینی بۆ زمانی تورکی، جەلادەت عەلی بەدرخان لە ساڵی ١٩٣٢ ئەلفوبێیەکی لاتینیی بۆ زمانی کوردی داھێنا کە ئێستا بە ناوی "ئەلفوبێی ھاوار" یان "بەدرخان" دەناسرێت. 
"""


font_file = os.path.expanduser("~/.local/share/fonts/fontamin/TrueType/Estedad-FD/Estedad_FD_Thin.ttf")

word_cloud = WordCloud(font_path=font_file, collocations = False, background_color = 'white', stopwords=ckb_stopwords).generate(text)
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show(block=True)