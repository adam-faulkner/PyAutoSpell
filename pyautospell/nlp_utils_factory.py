from pyautospell.simple_tokenizer import SimpleTokenizer

class NLPUtilsFactory(object):
    tokenizer = None
    def get_tokenizer(self):
        return self.tokenizer

class TokenizerFactory(object):
    def create_tokenizer(self, typ):
        tokenizer_objects = {'simple': SimpleTokenizer}  # add others
        return tokenizer_objects[typ]()
