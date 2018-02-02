# PyAutoSpell


Why yet another spellchecker in Python? I was looking for quick pre-processing component for text files that would identify misspellings and automatically incorporate confidence-weighted candidate corrections into a final, corrected text. Not finding anything that fit bill, I wrote PyAutoSpell. Given a potentially misspelled text, PyAutoSpell identifies any misspellings in the text, generates a set of candidate corrections for the misspelling, and then uses an ngram model to determine the probability that a given candidate correction is the best correction for that misspelling. It then incorporates the highest probability correction into the final, corrected text. 

## Setup


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
    print("original text ", corrections.original_text)
    print("corrected text ",corrections.corrected_text)
```
Result:
```
misspelled :  beleif
misspelled :  exprience
misspelled :  Lonon
misspelled :  beutiful
original text   It is my beleif, Watson, founded upon my exprience, that the lowest and vilest alleys in Lonon do not present 
     a more dreadful record of sin than does the smiling and beutiful countryside
corrected text   It is my belief, Watson, founded upon my experience, that the lowest and vilest alleys in London do not present 
     a more dreadful record of sin than does the smiling and beautiful countryside
```
