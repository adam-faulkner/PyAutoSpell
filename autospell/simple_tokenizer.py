import re

from autospell.word import Word


#TODO: there should be Tokenizer abstract class for this to extend
class SimpleTokenizer(object):
    def __init__(self):
        pass

    def tokenize(self, line : str):
        words = list()
        if (line == None or len(line.strip()) == 0):
            return list()
        #s  = None
        #try:
        #s = Sentence(line)
        #except:
         #   return None

        pattern = re.compile("[\\w']+|[^\\w\\s]+")
        matches = re.finditer(pattern, line)
        for match in matches:
            #print(match)
            wd = Word(line[match.start():match.end()], match.start(), match.end())
            words.append(wd)

        return words



def main():
    tokenizer = SimpleTokenizer()
    s = "I didn't think about John's new fish and that was miss-attributed to him."
    s2 = "what do you mean?"
    all_words =  tokenizer.tokenize(s)
    print([w.word for w in all_words])
    all_words2= tokenizer.tokenize(s2)
    print([w.word for w in all_words2])



#main()