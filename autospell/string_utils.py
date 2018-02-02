import string

class StringUtils(object):
    def __init__(self):
        self.not_check_if_contains_punct = set()
        self.punct_array = list("`~!@#$%^&*()_-+={}[]|\\:;\"'<>,.?/")
        self.puncts = set()
        for c  in self.punct_array:
            self.puncts.add(c)
        self.if_contains = list("(){}[]<>")
        self.not_check_if_contains_punct = set()
        for c in self.punct_array:
          self.not_check_if_contains_punct.add(c)
        self.non_check_words = set(["'s", "'t"])

    def should_not_check_single_char(self, c : str) -> bool:
        return c not in  string.ascii_lowercase+string.ascii_uppercase

    def should_not_check_string(self, w : str) -> bool:
        lowerw = w.lower()
        if w in self.puncts:
            return True
        if self.__is_all_punct(w):
            return True
        if self.contains_no_check_puncts(w):
          return True
        if self.__is_non_check_words(lowerw):
         return True
        if self.__has_non_check_prefix(lowerw):
          return True
        return False


    def __has_non_check_prefix(self, w : str) -> bool:
        if w.startswith("http:"):
            return True
        if w.startswith("www."):
            return True
        if w.startswith("@"):
          return True
        if w.startswith("#"):
          return True
        return False

    def __is_non_check_words(self, w : str) -> bool:
        if w in self.non_check_words:
            return True
        return False

    def contains_no_check_puncts(self, w : str) -> bool:
        for c in list(w):
            if c in self.not_check_if_contains_punct:
                return True
        return False


    def __is_all_punct(self, w : str) -> bool:
        for i in range(len(w)):
            if w[i]  in self.puncts:
                return True
        return False


def main():
    su = StringUtils()
    print(su.should_not_check_string("?"))

#main()