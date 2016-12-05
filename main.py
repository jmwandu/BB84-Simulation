"""
Joshua Mwandu, Max Taylor II
BB-84 Protocol Simulator
Fall 2016 Mathematics Research Project
4 December, 2016
"""
import sys
from math import ceil
from random import randint, random, sample
from multiprocessing import Pool

Alice = {'generatedBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
Bob = {'measuredBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
Eve = {'measuredBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
correct_basis_indeces = []
BITSIZE = 1000

#step 1 of protocol
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

#step 2 and 3 of protocol
def step2_3():
    #go from Alice to Eve
    temp_bit_list_Eve = []
    temp_basis_list_Eve = []
    for i in range(0, BITSIZE):
        random_basis = randint(0,1)
        if (random_basis == 0):
            temp_basis = 'X'
        elif (random_basis == 1):
            temp_basis = 'Z'
        
        temp_basis_list_Eve.append(temp_basis)
        
        if (Alice['chosenBases'][i] == temp_basis):
            temp_bit_list_Eve.append(Alice['generatedBits'][i])
        else:
            temp_bit_list_Eve.append(randint(0,1))
            
    Eve['measuredBits'] = temp_bit_list_Eve
    Eve['chosenBases'] = temp_basis_list_Eve
    
    #do same thing, but now go from Eve to Bob
    temp_bit_list_Bob = []
    temp_basis_list_Bob = []
    for i in range(0, BITSIZE):
        random_basis = randint(0,1)
        if (random_basis == 0):
            temp_basis = 'X'
        elif (random_basis == 1):
            temp_basis = 'Z'
        
        temp_basis_list_Bob.append(temp_basis)
        
        if (Eve['chosenBases'][i] == temp_basis):
            temp_bit_list_Bob.append(Eve['measuredBits'][i])
        else:
            temp_bit_list_Bob.append(randint(0,1))
            
    Bob['measuredBits'] = temp_bit_list_Bob
    Bob['chosenBases'] = temp_basis_list_Bob
    
#step 4 and 5 of protocol
def step4_5():
    for i in range(0, BITSIZE):
        if (Alice['chosenBases'][i] == Bob['chosenBases'][i]):
            correct_basis_indeces.append(i)

#threading for step 6 of the protocol
def step6_threading(received):
    lower = received[0]
    upper = received[1]
    
    bit_list_alice = []
    basis_list_alice = []
    bit_list_bob = []
    basis_list_bob = []
    bit_list_eve = []
    basis_list_eve = []
    
    for i in range(lower, upper):
        if (i in correct_basis_indeces):
            bit_list_alice.append(Alice['generatedBits'][i])
            basis_list_alice.append(Alice['chosenBases'][i])
            bit_list_bob.append(Bob['measuredBits'][i])
            basis_list_bob.append(Bob['chosenBases'][i])
            bit_list_eve.append(Eve['measuredBits'][i])
            basis_list_eve.append(Eve['chosenBases'][i])
            
    return (bit_list_alice, basis_list_alice, bit_list_bob, basis_list_bob, bit_list_eve, basis_list_eve)

#step 6 of the protocol        
def step6():
    input = [(0, int(BITSIZE/4)), 
            (int(BITSIZE/4), int(2*BITSIZE/4)), 
            (int(2*BITSIZE/4), int(3*BITSIZE/4)), 
            (int(3*BITSIZE/4), BITSIZE)]
    
    pool = Pool(4)
    
    results = pool.map(step6_threading, input)
    
    temp_bit_list_alice = results[0][0] + results[1][0] + results[2][0] + results[3][0]
    temp_basis_list_alice = results[0][1] + results[1][1] + results[2][1] + results[3][1]
    temp_bit_list_bob = results[0][2] + results[1][2] + results[2][2] + results[3][2]
    temp_basis_list_bob = results[0][3] + results[1][3] + results[2][3] + results[3][3]
    temp_bit_list_eve = results[0][4] + results[1][4] + results[2][4] + results[3][4]
    temp_basis_list_eve = results[0][5] + results[1][5] + results[2][5] + results[3][5]
    
    Alice['siftedBits'] = temp_bit_list_alice
    Bob['siftedBits'] = temp_bit_list_bob
    Eve['siftedBits'] = temp_bit_list_eve
    Alice['siftedBases'] = temp_basis_list_alice
    Bob['siftedBases'] = temp_basis_list_bob
    Eve['siftedBases'] = temp_basis_list_eve
    
#step 7 of protocol
def step7():
    reveal_size = ceil(len(correct_basis_indeces)/2)
    
    random_sample_alice = [Alice['generatedBits'][i] for i in sorted(sample(range(len(Alice['generatedBits'])), reveal_size))]
    random_sample_bob = [Bob['measuredBits'][i] for i in sorted(sample(range(len(Bob['measuredBits'])), reveal_size))]
    
    counter = 0
    
    for i in range(reveal_size):
        if (random_sample_alice[i] == random_sample_bob[i]):
            counter += 1
            
    error_rate = 100 * counter / reveal_size
    
    print("Error rate: ", error_rate, "%")
    
#where all the magic happens
def detailedPresentation():
    #BITSIZE = bit_size
    
    print("Welcome!")
    print("This program will create a secure key using the BB84 Protocol.")
    input("Press enter to proceed to Step 1...\n")
    
    print("Step 1: Alice prepares a random string of bits and encodes them randomly in either the X or Z bases")
    step1()
    print("Alice's bits and bases:")
    print(Alice['generatedBits'])
    print(Alice['chosenBases'])
    input("Press enter to proceed to Step 2...\n")
    
    print("Step 2: Alice sends each qubit to Bob (intercepted and then resent by Eve)")
    print("Step 3: Bob randomly measures each qubit in either X or Z bases and records his results")
    step2_3()
    print("Eve's bits and bases:")
    print(Eve['measuredBits'])
    print(Eve['chosenBases'], "\n")
    print("Bob's bits and bases:")
    print(Bob['measuredBits'])
    print(Bob['chosenBases'])
    input("Press enter to proceed to Step 4...\n")
    
    print("Step 4: Bob publicly tells Alice what basis he measured each qubit in")
    print("Step 5: Alice tells Bob for which qubits he chose the correct basis")
    step4_5()
    print("Indeces of bits/bases that Alice and Bob have in common:")
    print(correct_basis_indeces)
    input("Press enter to proceed to Step 6...\n")
    
    print("Step 6: Alice and Bob delete all of their corresponding qubits for which the bases disagree (and Eve tries to)")
    step6()
    print("Alice's sifted key and bases:")
    print(Alice['siftedBits'])
    print(Alice['siftedBases'], "\n")
    print("Bob's sifted key and bases:")
    print(Bob['siftedBits'])
    print(Bob['siftedBases'], "\n")
    print("Eve's sifted key and bases:")
    print(Eve['siftedBits'])
    print(Eve['siftedBases'], "\n")
    print("Length of sifted raw key: ", len(Alice['siftedBits']))
    print("Percentage of reduction: ", (BITSIZE-len(Alice['siftedBits']))/BITSIZE*100,"%")
    input("Press enter to proceed to Step 7...\n")
    
    print("Step 7: Alice and Bob agree on a small subset of the sifted raw key to publicly reveal")
    print("Note: This is to calculate the quantum bit error rate.")
    step7()
    input("Press enter to proceed to Step 8...\n")
    
    '''
    print("Step 8: Alice and Bob perform error reconciliation")
    input("Press enter to proceed to Step 9...\n")
    
    print()"Step 9: Alice and Bob perform primary amplification"
    input("Press enter to exit the program.")
    '''

def quickPresentation(bit_size):
    BITSIZE = bit_size
    step1()
    step2_3()
    step4_5()
    step6()
    step7()
    
def quickSimulation(bit_size):
    BITSIZE = bit_size
    print("some stuff")


if __name__ == "__main__":
    arg = sys.argv
    
    if (arg[1] == '0'):
        done = False
        
        while (not done):
            print("1: Run a detailed presentation (small bit size)")
            print("2: Run a \"quick\" presentation (large bit size)")
            print("3: Quit")
            userInput = input("What would you like to do? ")
            if (userInput == '1'):
                userInput =  input("What would you like the bit size to be? (Recommended: small)\n")
                detailedPresentation()
            elif (userInput == '2'):
                userInput =  input("What would you like the bit size to be? (Recommended: large)\n")
                quickPresentation(int(userInput))
            elif (userInput == '3'):
                done = True
                
        print("Goodbye!")
        
    elif (arg[1] == '1'):
        quickSimulation(arg[2])