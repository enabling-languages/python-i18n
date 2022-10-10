# Regex patterns

## Graphemes

`pattern = r'(\X)'`

## Myanmar syllables

1. ReSegment: `pattern = r'(?:(?<!္)([က-ဪဿ၊-၏]|[၀-၉]+|[^က-၏]+)(?![ှျ]?[့္်]))'`
2. sylbreak and myWord: 
    ```py
    myConsonant = r"က-အ"
    enChar = r"a-zA-Z0-9"
    otherChar = r"ဣဤဥဦဧဩဪဿ၌၍၏၀-၉၊။!-/:-@[-`{-~\s"
    ssSymbol = r'္'
    aThat = r'်'
    pattern = re.compile(r"((?<!" + ssSymbol + r")["+ myConsonant + r"](?![" + aThat + ssSymbol + r"])" + r"|[" + enChar + otherChar + r"])")
    ```



## Resources:

* https://medium.com/computronium/text-segmentation-7150cc58cb03 : `re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", raw)`
* https://goodboychan.github.io/python/datacamp/natural_language_processing/2020/07/15/01-Regular-expressions-and-word-tokenization.html
* https://web.stanford.edu/~jurafsky/slp3/old_oct19/2.pdf
* https://www.kaggle.com/discussions/general/331411