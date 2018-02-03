import re
from autospell.word import Word

class SimpleTokenizer(object):
    def __init__(self):
        pass

    def tokenize(self, line : str):
        '''
        :param line:
        :return: list of Word objects
        '''
        words = list()
        if (line == None or len(line.strip()) == 0):
            return list()
        pattern = re.compile("[\\w']+|[^\\w\\s]+")
        matches = re.finditer(pattern, line)
        for match in matches:
            wd = Word(line[match.start():match.end()], match.start(), match.end())
            words.append(wd)
        return words
