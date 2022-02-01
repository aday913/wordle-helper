import argparse
import logging

from english_words import english_words_lower_alpha_set
from itertools import combinations

class Helper(object):
    '''
    '''

    def __init__(self, state, letters, nonletters, debug):
        if debug:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(name)s: %(message)s')
            logging.debug('DEBUG-level logging')
        else:
            logging.basicConfig(level=logging.INFO,
                                format='%(name)s: %(message)s')
        
        # Check to ensure that the input state is 5 chars long
        if len(state) == 5:
            logging.info(f'Given initial state: {state}')
        else:
            raise ValueError('State should have length 5')
        self.nonLetters = nonletters
        logging.info(f'Letters not in solution: {self.nonLetters}')

        # Make a dictionary of the letters with known locations (the state)
        self.state = {}
        for i in range(len(state)):
            if state[i] != '_':
                self.state[state[i].lower()] = i
        self.stateKeys = [i for i in self.state.keys()]
        logging.debug(f'Dictionary representation of state: {self.state}')
        
        # Make a dictionary of the known letters and the locations
        # we know they're not located in
        self.knownLetters = {}
        for i in letters:
            self.knownLetters[i[0].lower()] = [int(num) for num in i[1:]]
        logging.info(
            f'''Letters known to be in solution: {
                [i for i in self.knownLetters.keys()]}'''
                )

        # Get all the 5 letter words
        self.words = self.getAllWords()

    def getAllWords(self):
        '''
        Returns all five-letter words in the english language as a list
        '''
        allWords = list(english_words_lower_alpha_set)
        words = [i for i in allWords if len(i) == 5]
        words.remove('u.s.a')   # 'u.s.a' considered a word for some reason
        logging.debug(f'Number of five letter words: {len(words)}')
        return words

    def filterState(self):
        '''
        Removes words from the list of possible solutions given the current
        state of the solution.
        '''
        iterable = self.words.copy()
        for word in iterable:
            logging.debug(f'Checking if {word} matches current state')
            # print(f'Checking if {word} matches current state')
            for key in self.state:
                if word[self.state[key]] != key and word in self.words:
                    self.words.remove(word)
        logging.info(f'After state filter, {len(self.words)} words remain')
        return
    
    def filterNonLetters(self):
        '''
        Removes words from the list of possible solutions given the nonletters
        list global variable.
        '''
        if len(self.nonLetters) == 0:
            logging.info('No non-letters known, skipping filter')
            return

        logging.info('We know some non-letters. Filtering now...')
        iterable = self.words.copy()
        for word in iterable:
            logging.debug(f'Checking presense of non-letter in {word}')
            for letter in word:
                if letter in self.nonLetters and word in self.words:
                    logging.debug(f'Removing {word}')
                    self.words.remove(word)
        logging.info(
            f'After non-letter filter, {len(self.words)} words remaining'
            )
        return

    def filterKnownLetterS(self):
        '''
        Removes words that don't contain letters that we know exist but don't
        know where they are supposed to be placed.
        '''
        if self.knownLetters == {}:
            logging.info('No other letters known, skipping filter')
            return
        
        logging.info('We know some letters. Filtering now...')

        # First we can filter all words that don't contain the known letters
        iterable = self.words.copy()
        for word in iterable:
            for letter in self.knownLetters.keys():
                if letter not in word and word in self.words:
                    self.words.remove(word)
        
        # Next remove cases where the letter is in a non-location:
        iterable = self.words.copy()
        for word in iterable:
            for letter in self.knownLetters.keys():
                for index in self.knownLetters[letter]:
                    if word[index] == letter and word in self.words:
                        self.words.remove(word)
        logging.info(
            f'After known letters filter, {len(self.words)} words remain'
            )

    def analyzePossibleLetters(self):
        '''
        
        '''
        numWords = len(self.words)
        alphabet = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
            'y', 'z'
        ]
        letters = {}
        for i in alphabet:
            letters[i] = 0

        for word in self.words:
            usedLetters = []
            for letter in word:
                if letter not in usedLetters:
                    letters[letter] += 1
                    usedLetters.append(letter)

        combos = combinations(alphabet, 5)
        values = {}
        for i in list(combos):
            values[''.join(i)] = 0
        for key in values:
            for i in key:
                values[key] += (letters[i]/numWords)
        values = dict(
            sorted(values.items(), key=lambda item: item[1], reverse=True)
            )
        return values

    def findWord(self, testLetters):
        '''
        Given a list of test letters, will try to find a word with all five
        '''
        firstWord = None
        for word in self.words:
            goodLetters = [i for i in testLetters]
            for letter in word:
                if letter in goodLetters:
                    goodLetters.remove(letter)
            if len(goodLetters) == 0:
                firstWord = word
                return True, firstWord
        return False, None

    def run(self):
        '''
        
        '''
        # First let's filter out all non-possible words
        self.filterState()
        self.filterNonLetters()
        self.filterKnownLetterS()

        logging.info(
            f'Number of possible words after filtering: {len(self.words)}'
            )
        if len(self.words) == 0:
            logging.info(
                f'No words possible given the input parameters.'
                )
            return None
        if len(self.words) < 11:
            logging.info(
                f'Low amount of words! Here is what is possible: {self.words}'
                )
        
        # Now we can run a letter analysis for find the next best word:
        values = self.analyzePossibleLetters()
        for key in values:
            check, word = self.findWord([char for char in key])
            if check:
                logging.debug(f'Best combination of letters: {key}')
                logging.info(f'Best word to use: {word}')
                return word
        logging.info('No solution found!')
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Wordle daily challenge helper. Given a current game 
        state and known letters/positions, the helper will provide the best 
        next guess for the user.'''
    )

    parser.add_argument('-s', '--state', type=str, required=True, 
                    help='State of the wordle challenge. Example: _r__l')
    parser.add_argument('-k', '--knownletters', required=False, default=[],
                help='Known letters and the locations we know they are not in', 
                    nargs='+')
    parser.add_argument('-n', '--nonletters', required=False, default='',
                    help='Letters not in solution')
    parser.add_argument('-d', '--debug', required=False, default=False,
                    help='Bool to turn on debugger', type=bool)

    args = parser.parse_args()

    helper = Helper(
        args.state,
        args.knownletters,
        args.nonletters,
        args.debug
        )

    helper.run()