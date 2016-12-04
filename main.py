import random

Alice = {'generatedBits':None, 'chosenBases':None}
Bob = {'measuredBits':None, 'chosenBases':None}

def main():
    done = False
    
    while(not done):
        print Alice.keys()
        print Bob.keys()
        Alice['generatedBits'] = (0,0,0)
        Alice['chosenBases'] = ('x', 'z', 'x')
        print "Alice data: ", Alice
        done = True
        
if __name__ == "__main__":
    main()