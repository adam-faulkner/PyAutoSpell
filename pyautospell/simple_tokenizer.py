import re
from pyautospell.word import Word

class SimpleTokenizer(object):
    def __init__(self):
        pass

    def tokenize(self, line):
        '''
        :param line:
        :return: list of Word objects
        '''
        words = list()
        if (line == None):
            return list()
        pattern = re.compile("[\\w']+|[^\\w\\s]+")
        matches = re.finditer(pattern, line)
        for match in matches:
            wd = Word(line[match.start():match.end()], match.start(), match.end())
            words.append(wd)
        return words
