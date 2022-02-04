# wordle-helper
### Python program to help solve daily [Wordle](https://www.powerlanguage.co.uk/wordle/) challenges!
---
Given a information about the current state of the challenge and known parameters (letters known to not be in the solution or letters that are known to be in the solution but don't know where), the bot will produce the best next word to guess given all the possible words left!  

Example input:  

```
C:path> python helper.py -s _o___ -k c4 -n arsetni
```

In the above example, we know the "o" is in the second letter location, that there is a "c" in the solution but that it isn't in location 5 (0-index), and that none of the letters in "arsetni" are in the final solution.  

Given these inputs, the following output would be expected:  

```
root: Given initial state: _o___
root: Letters not in solution: arsetni
root: Letters known to be in solution: ['c']
root: After state filter, 403 words remain
root: We know some non-letters. Filtering now...
root: After non-letter filter, 48 words remaining
root: We know some letters. Filtering now...
root: After known letters filter, 14 words remain
root: Number of possible words after filtering: 14
root: Best word to use: pouch
```  

Also included in the [Analysis](https://github.com/aday913/wordle-helper/blob/main/analysis.ipynb) Jupyter notebook is data analysis pointing to the best possible initial wordle guess. Go find out what it is!

The next step will be to implement a "player" object that plays through all possible five-letter words of the English language to determine whether the bot could "win" these challenges every day (ie not take more than 6 tries). If this is the case, then we will have developed a fully successful bot!  

