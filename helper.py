import logging

from english_words import english_words_lower_alpha_set

class Helper(object):
    '''
    '''

    def __init__(self, debug=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(name)s: %(message)s')
            logging.debug('DEBUG-level logging')
        else:
            logging.basicConfig(level=logging.INFO,
                                format='%(name)s: %(message)s')
        self.words = self.getAllWords()

    def getAllWords(self):
        '''
        '''
        allWords = list(english_words_lower_alpha_set)
        words = [i for i in allWords if len(i) == 5]
        logging.debug(f'Number of five letter words: {len(words)}')
        return words

if __name__ == '__main__':
    Helper(debug=True)