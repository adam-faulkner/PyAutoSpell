from abc import ABC, abstractmethod


class SpellChecker(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def check_spelling(self, text, num_suggestions):
        '''
        :param text:
        :param num_suggestions:
        :return: a list of objects of type misspelling
        '''
        pass

    @abstractmethod
    def check_spelling(self, text, num_suggestions):
        '''
        :param text:
        :param num_suggestions:
        :return: a list of objects of type Misspelling
        '''
        pass

    @abstractmethod
    def check_word(self, text, num_suggestions):
        '''
         Given a single word (no tokenization) return the corrected version
        :param text:
        :param num_suggestions:
        :return: an object of type Misspelling, which comtains the misspelled word and
        corrections
        '''
        pass

    @abstractmethod
    def correct_spelling(self, text):
        '''
        :param text:
        :return: object of type Correction
        '''
        pass

    @abstractmethod
    def in_dict(self, text):
        '''
        Is the word in the dictionary?
        :param text:
        :return: boolean
        '''
        pass