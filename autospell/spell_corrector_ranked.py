from autospell.spellchecker import SpellChecker
from autospell.correction import Correction
from autospell.IFL_suggestion_selector import IFLSuggestionSelector

class SpellCorrectorRanked(SpellChecker):

    def __init__(self, checker, suggestion_selector, suggestion_scorer):
        self.spell_checker = checker
        self.suggestion_selector = IFLSuggestionSelector()
        self.candidate_scorer = suggestion_scorer

    def check_word(self, text, suggestions_count):
        '''
        :param text:
        :param suggestions_count:
        :return:
        '''
        return self.spell_checker.check_word(text, suggestions_count)


    def correct_spelling(self, text):
        '''
        :param text:
        :return: object of type Correction
        '''
        misspellings = self.spell_checker.check_spelling(text, 10)
        self.candidate_scorer.candidate_scoring(misspellings, text)
        corrected = self.suggestion_selector.select(text, misspellings)
        return Correction(text,corrected, misspellings)

    def in_dict(self, text):
        '''
        Is the word in the dictionary?
        :param text:
        :return: boolean
        '''
        return False

    def check_spelling(self, text, num_suggestions):
        '''
        :param text:
        :param num_suggestions:
        :return: a list of objects of type Misspelling
        '''
        return self.spell_checker.check_spelling(text, num_suggestions)