"""
Joshua Mwandu, Max Taylor II
BB-84 Protocol Simulator
Fall 2016 Mathematics Research Project
4 December, 2016
"""
from random import randint
import os

Alice = {'generatedBits':[], 'chosenBases':[]}
Bob = {'measuredBits':[], 'chosenBases':[]}
Eve = {'measuredBits':[], 'chosenBases':[]}
BITSIZE = 10

def step1():
    temp_bit_list = []
    temp_basis_list = []
    for i in range(0, BITSIZE):
        random_bit = randint(0,1)
        random_basis = randint(0,1)
        
        temp_bit_list.append(random_bit)
        
        if (random_basis == 0):
            temp_basis_list.append('X')
        elif (random_basis == 1):
            temp_basis_list.append('Z')
            
    Alice['generatedBits'] = temp_bit_list
    Alice['chosenBases'] = temp_basis_list
    
def step2_3():
    temp_bit_list = []
    temp_basis_list = []
    for i in range(0, BITSIZE):
        random_basis = randint(0,1)
        if (random_basis == 0):
            temp_basis = 'X'
        elif (random_basis == 1):
            temp_basis = 'Z'
        
        temp_basis_list.append(temp_basis)
        
        if (Alice['chosenBases'][i] == temp_basis):
            temp_bit_list.append(Alice['generatedBits'][i])
        else:
            temp_bit_list.append(randint(0,1))
            
    Bob['measuredBits'] = temp_bit_list
    Bob['chosenBases'] = temp_basis_list

#where all the magic happens
def main():
    done = False
    
    while(not done):
        
        print "Welcome!"
        print "This program will create a secure key using the BB84 Protocol."
        raw_input("Press enter to proceed to Step 1...")
        
        print "Step 1: Alice prepares a random string of bits and encodes them randomly in either the X or Z bases"
        step1()
        print Alice
        raw_input("Press enter to proceed to Step 2...")
        
        print "Step 2: Alice sends each qubit to Bob"
        print "Step 3: Bob randomly measures each qubit in either X or Z bases and records his results"
        step2_3()
        print Bob
        raw_input("Press enter to proceed to Step 4...")
        
        '''
        print "Step 4: Bob publicly tells Alice what basis he measure each quit in"
        print "Step 5: Alice tells Bob for which qubits he chose the correct basis"
        raw_input("Press enter to proceed to Step 6...")
        
        print "Step 6: Alice and Bob delete all of their corresponding qubits for which the bases disagree"
        raw_input("Press enter to proceed to Step 7...")
        
        print "Step 7: Alice and Bob agree on a small subset of the sifted raw key to publicly reveal"
        print "Note: This is to calculate the quantum bit error rate."
        raw_input("Press enter to proceed to Step 8...")
        
        print "Step 8: Alice and Bob perform error reconciliation"
        raw_input("Press enter to proceed to Step 9...")
        
        print "Step 9: Alice and Bob perform primary amplification"
        raw_input("Press enter to exit the program.")
        '''
        
        done = True
        
if __name__ == "__main__":
    main()