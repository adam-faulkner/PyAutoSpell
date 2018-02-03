class Correction(object):

    def __init__(self,original_text,  corrected_text,  misspellings):
        '''
        :param original_text:
        :param corrected_text:
        :param misspellings:
        '''
        self.corrected_text = corrected_text
        self.original_text = original_text
        self.misspellings = misspellings



