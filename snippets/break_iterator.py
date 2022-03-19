####################
#
# Break Iterator
#   © Enabling Languages 2022
#   Released under the MIT License.
#
####################

from icu import BreakIterator, Locale

l = "en_AU"

if l in BreakIterator.getAvailableLocales():
    DEFAULT_LOC = Locale(l)
else:
    DEFAULT_LOC = Locale.getRoot()
  
def iterate_breaks(text, break_iterator):
    break_iterator.setText(text)
    lastpos = 0
    while True:
        next_boundary = break_iterator.nextBoundary()
        if next_boundary == -1: return
        yield text[lastpos:next_boundary]
        lastpos = next_boundary
        
text=""

# character, word, line, title, and sentence instances
#   createCharacterInstance()
#   createLineInstance()
#   createSentenceInstance()
#   createTitleInstance()
#   createWordInstance()
bi = BreakIterator.createCharacterInstance(DEFAULT_LOC)
list(iterate_breaks(text, bi))
