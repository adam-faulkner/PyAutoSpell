from autospell.spellchecker import SpellChecker
from autospell.simple_tokenizer import SimpleTokenizer
from autospell.nlp_utils_factory import NLPUtilsFactory
from autospell.suggestion_scorer import SuggestionScorer
from autospell.hunspell_checker import HunspellChecker
from autospell.suggestion_scorer_lm import SuggestionScorerLM
from autospell.IFL_suggestion_selector import IFLSuggestionSelector
from autospell.spell_corrector_ranked import SpellCorrectorRanked
from autospell.misspelling import Misspelling
from autospell.nlp_utils_factory import TokenizerFactory


class AutoChecker(SpellChecker):

    def __init__(self, builder):

        self.bad_chars_map = {}
        self.spell_checker = None
        self.suggestion_scorer = SuggestionScorer
        self.builder = builder
        self.tokenizer = SimpleTokenizer
        self.language_model = builder.language_model
        self.dictionary = builder.dictionary
        self.dictionary_name = builder.dictionary_name
        self.spell_check_obj = None
        if self.builder.spell_checker == None:
            self.spell_check_obj = HunspellChecker.Builder().dictionary(self.dictionary_name, self.builder.dictionary).build()
        else:
            self.spell_check_obj = builder.spell_checker
        self.lm_path = builder.language_model
        self.suggestion_scorer =  SuggestionScorerLM(builder.tokenizer, self.lm_path)# // TODO
        self.suggestion_selector = IFLSuggestionSelector()
        self.spell_corrector = SpellCorrectorRanked(self.spell_check_obj, self.suggestion_selector, self.suggestion_scorer)

    def score_suggestion(self, suggestion : Misspelling.Suggestion, line : str):
        prob = self.suggestion_scorer.score_suggestion(suggestion, line)
        return prob

    def check_word(self, text , suggestions_count):
        return self.spell_corrector.check_word(text, suggestions_count)

    def check_spelling(self, text : str, suggestions_count):
        filteredText = text.replace("n\\?t", "n't")
        misspellings = self.spell_corrector.check_spelling(filteredText, suggestions_count)
        print("misspellings ", misspellings)
        return misspellings

    def in_dict(self, text):
        '''
        Is the word in the dictionary?
        :param text:
        :return: boolean
        '''
        return False

    def correct_spelling(self, text):
        correction = self.spell_corrector.correct_spelling(text)
        return correction



    class Builder(object):
        def __init__(self):
            self.dictionary
            self.dictionary_name
            self.aff_files = set()
            self.language_model
            self.language_models_pos = set()
            self.confusion_set = list()
            self.vocab_file = set()
            self.unigram = set()
            self.tokenizer = SimpleTokenizer()
            self.gamma = 1.0
            self.spell_checker

        def spell_checker(self, spell_checker):
            self.spell_checker = spell_checker
            return self

        def aff_files(self,path):
            self.aff_files.add(path)
            return self


        def dictionary(self, path):
            self.dictionary = path
            return self

        def dictionary_name(self, name):
            self.dictionary_name = name
            return self

        def language_model(self, path):
            self.language_model = path
            return self

        def confusion_set(self, confusion_set):
            self.confusionSet = confusion_set
            return self

        def vocab_file(self,  path):
            self.vocab_file.add(path)
            return self

        def featurized_unigram(self, path):
            self.unigram.add(path)
            return self

        def language_model_pos(self, path):
            self.language_models_pos.add(path)
            return self

        def set_tokenizer(self, tokenizer):
            self.tokenizer = tokenizer
            return self

        def build(self):
            if self.tokenizer == None:
                factory = TokenizerFactory()
                self.tokenizer = factory.create_tokenizer("simple")
            return AutoChecker(self)

