import argparse
import logging

from english_words import english_words_lower_alpha_set

class Helper(object):
    '''
    '''

    def __init__(self, state, letters, debug):
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
    parser = argparse.ArgumentParser(
        description='''Wordle daily challenge helper. Given a current game 
        state and known letters/positions, the helper will provide the best 
        next guess for the user.'''
    )

    parser.add_argument('-s', '--state', type=str, required=True, 
                    help='State of the wordle challenge. Example: _r__l')
    parser.add_argument('-l', '--letters', required=False, default='',
                    help='Known letters without known locations')
    parser.add_argument('-d', '--debug', required=False, default=False,
                    help='Bool to turn on debugger', type=bool)

    args = parser.parse_args()

    helper = Helper(
        args.state,
        args.letters,
        args.debug
        )
