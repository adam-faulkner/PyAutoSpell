from abc import ABC, abstractmethod

class SuggestionScorer(ABC):
    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def candidate_scoring(self, misspelllist,text):
        pass

    @abstractmethod
    def score_suggestion(self, suggestion,line, misspelling=None):
        pass

