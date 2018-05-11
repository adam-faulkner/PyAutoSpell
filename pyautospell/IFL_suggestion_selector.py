from pyautospell.suggestion_selector import SuggestionSelector

class IFLSuggestionSelector(SuggestionSelector):

    @staticmethod
    def select(text, misspellings):
        '''
        Takes a list of Misspelling objects with rank-ordered suggestions
        and incorporates the top-ranked suggestion into text. Returns
        the corrected text.

        :param text: str
        :param misspellings: list of Misspelling objects
        :return: corrected text
        '''
        sb = text
        shift = 0
        for m in  misspellings:
            best = IFLSuggestionSelector.best(m.suggestions)
            if best == None:
                pass
            start = m.begin + shift
            end = m.end + shift
            length = m.end - m.begin + 1
            correct = best.text
            sb = sb[:start]+correct+sb[end:]
            shift += len(correct) + 1 - length
        return sb

    @staticmethod
    def best(suggestion_list):
        '''
        :param suggestion_list:
        :return:
        '''
        best = suggestion_list[0]
        #for s in  suggestion_list:
        #    if best == None or s.weight > best.weight:
         #       best = s
        return best

