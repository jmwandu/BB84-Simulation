"""
Joshua Mwandu, Max Taylor II
BB-84 Protocol Simulator
Fall 2016 Mathematics Research Project
4 December, 2016
"""

import random

Alice = {'generatedBits':None, 'chosenBases':None}
Bob = {'measuredBits':None, 'chosenBases':None}
Eve = {'measuredBits':None, 'chosenBases':None}

#where all the magic happens
def main():
    done = False
    
    while(not done):
        
        print "Welcome!"
        userInput = raw_input("Press enter to continue...")
        
        Alice['generatedBits'] = (0,0,0)
        Alice['chosenBases'] = ('x', 'z', 'x')
        print "Alice data: ", Alice
        done = True
        
if __name__ == "__main__":
    main()