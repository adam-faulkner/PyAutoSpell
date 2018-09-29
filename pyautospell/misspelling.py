from enum import Enum

class Misspelling(object):

    class MisspellingType(Enum):
        SPELLING = 1
        SPELLINGRW = 2
        REPEATEDWORD = 3

    def __init__(self):
        self.begin = int()
        self.end = int()
        self.word = ""
        self.type = self.MisspellingType.SPELLING
        #array of Suggestion objects
        self.suggestions = list()
        self.suggestion = self.Suggestion

    def clear_suggestions(self):
        self.suggestions.clear()

    def get_suggestions_sorted(self):
        self.suggestions.sort(key=lambda x: x.weight)
        return self.suggestions

    def add_suggestion(self, suggestion=None,suggestion_text=None, weight = None, key=None):
        '''
        :param suggestion:
        :param suggestion_text:
        :param weight:
        :param key:
        :return:
        '''
        if isinstance(suggestion_text, str): 
            if suggestion_text is not None:
                self.suggestions.append(self.Suggestion(suggestion_text,1.0))
            if suggestion is not None:
                self.suggestions.append(suggestion)
            if suggestion_text is not None and weight is not None:
                self.suggestions.append(self.Suggestion(suggestion_text, weight))
            if suggestion_text is not None and weight is not None and key is not None:
                self.suggestions.append(self.Suggestion(suggestion_text, weight, checker_name=key))

    def to_string(self):
        return "Misspelling [word=" + self.word + ", suggestions=" + " , ".join([s.text for s in self.suggestions]) + "]"


    class Suggestion(object):

        def __init__(self, text, weight, checker_name=None, apriori=1.0):
            '''
            :param text:
            :param weight:
            :param checker_name:
            :param apriori:
            '''
            self.text  = text
            self.weight = weight
            self.apriori = apriori
            self.misspelling = Misspelling
            self.checker_name = checker_name

        def to_string(self):
            return self.text + ":" + self.weight + ":" + self.checker_name
