import hunspell
from pyautospell.spellchecker import SpellChecker
from pyautospell.string_utils import StringUtils
from pyautospell.misspelling import Misspelling
from pyautospell.word import Word
from pyautospell.IFL_suggestion_selector import IFLSuggestionSelector
from pyautospell.simple_tokenizer import SimpleTokenizer
from pyautospell.nlp_utils_factory import TokenizerFactory
from pyautospell.misspelling import Misspelling
from pyautospell.correction import Correction
import spacy

class HunspellChecker(SpellChecker):

    def __init__(self,builder ):
        '''
        :param builder:
        '''
        self.str_utils = StringUtils()
        self.checker = builder.checker
        self.tokenizer = SimpleTokenizer()#builder.tokenizer
        self.suggestion_selector = IFLSuggestionSelector()
        self.TAB = "\t"
        self.dictionary = builder.checker
        #TODO: singletonize this
        self.nlp = spacy.load('en')
        self.suggestions_count = 10

    def check_spelling(self, text, num_suggestions):
        '''
        :param text:
        :param num_suggestions:
        :return:
        '''
        pass

    def in_dict(self, text):
        '''
        :param text:
        :return:
        '''
        return False

    def check_word(self,token, suggestions_count):
        '''
        :param token:
        :param suggestions_count:
        :return: Misspelling
        '''
        misspelling = Misspelling()
        if not self.dictionary.spell(token): #h.spell('incorect') -> False
            suggestions = self.dictionary.suggest(token)
            truncated_suggs = list()
            if len(suggestions)> suggestions_count:
                truncated_suggs = suggestions[0 :suggestions_count +1]
            misspelling.word = token
            misspelling.begin = 0
            misspelling.end = len(token)
            misspelling.type = Misspelling.MisspellingType.SPELLING
            rank = 0.0
            if truncated_suggs:
                for s in truncated_suggs:
                    rank +=1
                    misspelling.add_suggestion(s, rank)
            else:
                for s in suggestions:
                    rank +=1
                    misspelling.add_suggestion(suggestion_text=s, weight=rank)
        return misspelling

    def check_spelling(self, text, suggestions_count,merge=False):
        '''
        :param text:
        :param suggestions_count:
        :param merge:
        :return:
        '''
        misspelling_list  = list()
        tokens = self.tokenizer.tokenize(text)
        print (type(tokens))
        for token  in  tokens:
            if not token.word.strip():
                continue
            misspelling = self.check_word(token.word.strip(), self.suggestions_count)
            if not misspelling.suggestions:
                continue
            if (misspelling == None):
                continue
            elif self.__filter_misspelling(misspelling):
                continue
            misspelling.begin = token.start
            misspelling.end = token.end
            misspelling_list.append(misspelling)
        return misspelling_list

    def correct_spelling(self, text):
        '''
        :param text:
        :return: Correction
        '''
        misspellings = self.check_spelling(text, 10)
        return Correction(text, self.suggestion_selector.select(text,
        misspellings), misspellings)

    def __filter_misspelling(self, next):
        '''
        :param next:
        :return:
        '''
        #if (len(next.suggestions) == 1 and  len(next.suggestions.iterator().next().text) == 0):
         #   return True
        if (len(next.word) == 1 and self.str_utils.should_not_check_single_char(next.word[0].strip())):
            return True
        elif (self.str_utils.should_not_check_string(next.word.strip())):
            return True
        return False

    class Builder(object):
        def __init__(self):
            self.tokenizer
            #private Hunspell.Checker checker;
            self.checker = None
            self.dict_name = None

        def dictionary(self, name, path):
            self.checker = hunspell.Hunspell(name, hunspell_data_dir=path)
            return self

        def tokenizer(self, tokenizer):
            self.tokenizer = tokenizer
            return self

        def build(self):
            if (self.tokenizer is None):
                factory = TokenizerFactory()
                self.tokenizer = factory.create_tokenizer("simple")
            return HunspellChecker(self)
