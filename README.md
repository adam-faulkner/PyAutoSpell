# PyAutoSpell


Why yet another spellchecker in Python(YASP)? I was looking for a text pre-processing component that would (1) identify misspellings and provide candidate corrections and, (2) would automatically incorporate corrections into a final, corrected text using sophisticated techniques such as candidate-in-context re-ranking via ngram probabilities. While there are plenty of Python libraries that perform (1) reasonably well I've yet to come across anything that also does (2). So, I wrote PyAutoSpell. Given a potentially misspelled text, PyAutoSpell identifies any misspellings in the text, generates a set of candidate corrections for the misspelling, and then uses an ngram model to determine the probability that a given candidate correction is the best correction for that misspelling. It then incorporates the highest probability correction into the final, corrected text. 

## Setup

The following has been tested on OSX, High Sierra.

After cloning the project, `cd` to `PyAutoSpell` and then do

```python3 -m pip install -r requirements.txt```

(Note that I include `python3 -m` before my `pip` call since I have multiple pythons installed on my system and I want the package installed for my `python3` install; your setup might be different).

The `spacy` dependency requires an `en` language model. Do

```python3 -m spacy download en```

One installation pitfall that OSX users should be mindful of when installing the `CyHunspell` dependency: During install, you'll very likley get an `Operation not permitted` error when trying to install one of `CyHunspell`'s dependencies, `six`.  Deal with this by editing the above command as follows:

```python3 -m pip install -r requirements.txt --ignore-installed six```

You should confirm that `CyHunspell` and the rest of the dependencies listed in `requirements.txt` have been correctly installed by doing a `pip freeze` 

Then, install `PyAutoSpell` by doing 

```python3 -m pip install .```

Along with the python dependencies included in ```requirements.txt```, PyAutoSpell requires two additional resources: a hunspell dictionary and a [KenLM](https://github.com/kpu/kenlm) language model in binary format. The former is available from the [usual sources](http://wordlist.aspell.net/). (I've also included a recent `hunspell` english dict in the `resources` folder so you can go ahead and use that.) For demonstration purposes I've trained a relatively small (~53 million trigrams) KenLM model on a subset of Wikipedia, which you can access [here](https://www.dropbox.com/s/4p65y9uso9g3zrr/wiki_lm_truncated_c.klm?dl=0).  This model works reasonably well but you'll have to train a larger model if you want better performance. The usage example below assumes that both these files have been placed in the `resources` folder.


## Usage
```
Python 3.6.5 (default, Apr 25 2018, 14:23:58) 
[GCC 4.2.1 Compatible Apple LLVM 9.1.0 (clang-902.0.39.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyautospell
>>> from pyautospell.autochecker import AutoChecker
>>> spell_checker = AutoChecker.Builder().dictionary("./resources/hunspell-en_US-2018.04.16/").dictionary_name("en_US").language_model('./resources/wiki_lm_truncated_c.klm').build()
>>> auto_checker = AutoChecker(spell_checker)
 >>> corrections = auto_checker.correct_spelling("It is my beleif, Watson, founded upon my esperience, that the low3est and vilest alleys in London do noit present a more dr3eadful record of sin than does the smiling and beautiful countryside")
<class 'list'>
>>> misspellings = corrections.misspellings
>>> for misspelling in misspellings:
...         print("misspelled : ", misspelling.word)
... 
misspelled :  beleif
misspelled :  esperience
misspelled :  low3est
misspelled :  noit
misspelled :  dr3eadful
>>> print("corrected text: ",corrections.corrected_text)
corrected text:  It is my belief, Watson, founded upon my experience, that the lowest and vilest alleys in London do not present a more disregardful record of sin than does the smiling and beautiful countryside


