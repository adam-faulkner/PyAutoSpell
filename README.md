# PyAutoSpell


Why yet another spellchecker in Python? I was looking for quick pre-processing component for text files that would identify misspellings and automatically incorporate confidence-weighted candidate corrections into a final, corrected text. Not finding anything that fit bill, I wrote PyAutoSpell. Given a potentially misspelled text, PyAutoSpell identifies any misspellings in the text, generates a set of candidate corrections for the misspelling, and then uses an ngram model to determine the probability that a given candidate correction is the best correction for that misspelling. It then incorporates the highest probability correction into the final, corrected text. 

## Setup


## Usage


