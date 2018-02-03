# PyAutoSpell


Why yet another spellchecker in Python? I was looking for a text pre-processing component that would (1) identify misspellings and provide candidate corrections and, (2) would automatically incorporate confidence-weighted candidate corrections into a final, corrected text using sophisticated techniques such as candidate-in-context re-ranking via ngram probabilities. While there are plenty of Python libraries that perform (1) reasonably well I've yet to come across anything that also does (2). So, I wrote PyAutoSpell. Given a potentially misspelled text, PyAutoSpell identifies any misspellings in the text, generates a set of candidate corrections for the misspelling, and then uses an ngram model to determine the probability that a given candidate correction is the best correction for that misspelling. It then incorporates the highest probability correction into the final, corrected text. 

## Setup
```pip install requirements.txt```

Along with the python dependencies included in ```requirements.txt```, PyAutoSpell requires two additional resources: a hunspell dictionary and a [KenLM](https://github.com/kpu/kenlm) language model in binary format. The former is available from the [usual sources](http://wordlist.aspell.net/). For demonstration purposes I've trained a relatively small (53189736 trigrams) KenLM model on a subset of Wikipedia, which you can access [here](https://www.dropbox.com/s/4p65y9uso9g3zrr/wiki_lm_truncated_c.klm?dl=0).


## Usage
```
  #add path to hunspell dict and klm model
    spell_checker = AutoChecker.Builder().dictionary("./resources/hunspell-en_US-2017.01.2 /").dictionary_name("en_US").language_model('./resources/wiki_lm_truncated_c.klm').build()
    auto_checker = AutoChecker(spell_checker)
    txt = """ It is my beleif, Watson, founded upon my exprience, that the lowest and vilest alleys in Lonon do not present 
     a more dreadful record of sin than does the smiling and beutiful countryside"""
    #get a Correction object
    corrections = auto_checker.correct_spelling(txt)
    misspellings = corrections.misspellings
    for misspelling in misspellings:
        print("misspelled : ", misspelling.word)
    print("original text: ", corrections.original_text)
    print("corrected text: ",corrections.corrected_text)
```
Result:
```
misspelled :  beleif
misspelled :  exprience
misspelled :  Lonon
misspelled :  beutiful
original text:   It is my beleif, Watson, founded upon my exprience, that the lowest and vilest alleys in Lonon do not present 
     a more dreadful record of sin than does the smiling and beutiful countryside
corrected text:   It is my belief, Watson, founded upon my experience, that the lowest and vilest alleys in London do not present 
     a more dreadful record of sin than does the smiling and beautiful countryside
```
