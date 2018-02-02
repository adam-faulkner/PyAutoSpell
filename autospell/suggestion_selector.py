from abc import ABC, abstractmethod


class SuggestionSelector(ABC):
    def __init__(self,):
        super().__init__()

    @abstractmethod
    def select(self,text, misspelllist):
        pass
