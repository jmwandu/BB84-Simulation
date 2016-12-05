"""
Joshua Mwandu, Max Taylor II
BB-84 Protocol Simulator
Fall 2016 Mathematics Research Project
4 December, 2016
"""
import sys
from random import randint
from multiprocessing import Pool

Alice = {'generatedBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
Bob = {'measuredBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
Eve = {'measuredBits':[], 'chosenBases':[]}
correct_basis_indeces = []
BITSIZE = 100000

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
    
#step 4 and 5 of protocol
def step4_5():
    for i in range(0, BITSIZE):
        if (Alice['chosenBases'][i] == Bob['chosenBases'][i]):
            correct_basis_indeces.append(i)

#threading for step 6 of the protocol
def step6_threading(received):
    bit_list = received[0]
    basis_list = received[1]
    lower = received[2]
    upper = received[3]
    
    #num = 0
    
    for i in range(lower, upper):
        #num += 1
        #print(num)
        if (i in correct_basis_indeces):
            bit_list.append(Alice['generatedBits'][i])
            basis_list.append(Alice['chosenBases'][i])
            
    return (bit_list, basis_list)

#step 6 of the protocol        
def step6():
    bit_list1 = []
    basis_list1 =[]
    bit_list2 = []
    basis_list2 =[]
    bit_list3 = []
    basis_list3 =[]
    bit_list4 = []
    basis_list4 =[]
    
    input = [(bit_list1, basis_list1, 0, int(BITSIZE/4)), 
            (bit_list2, basis_list2, int(BITSIZE/4), int(2*BITSIZE/4)), 
            (bit_list3, basis_list3, int(2*BITSIZE/4), int(3*BITSIZE/4)), 
            (bit_list4, basis_list4, int(3*BITSIZE/4), BITSIZE)]
    
    pool = Pool(4)
    
    results = pool.map(step6_threading, input)
    
    temp_bit_list = results[0][0] + results[1][0] + results[2][0] + results[3][0]
    temp_basis_list = results[0][1] + results[1][1] + results[2][1] + results[3][1]
    
    Alice['siftedBits'] = temp_bit_list
    Bob['siftedBits'] = temp_bit_list
    Alice['siftedBases'] = temp_basis_list
    Bob['siftedBases'] = temp_basis_list

#where all the magic happens
def detailedPresentation():
    print("Welcome!")
    print("This program will create a secure key using the BB84 Protocol.")
    input("Press enter to proceed to Step 1...")
    
    print("Step 1: Alice prepares a random string of bits and encodes them randomly in either the X or Z bases")
    step1()
    print("Alice's bits and bases:")
    #print(Alice['generatedBits'])
    #print(Alice['chosenBases'])
    input("Press enter to proceed to Step 2...")
    
    print("Step 2: Alice sends each qubit to Bob")
    print("Step 3: Bob randomly measures each qubit in either X or Z bases and records his results")
    step2_3()
    print("Bob's bits and bases:")
    #print(Bob['measuredBits'])
    #print(Bob['chosenBases'])
    input("Press enter to proceed to Step 4...")
    
    print("Step 4: Bob publicly tells Alice what basis he measured each qubit in")
    print("Step 5: Alice tells Bob for which qubits he chose the correct basis")
    step4_5()
    print("Indeces of bits/bases that Alice and Bob have in common:")
    print(correct_basis_indeces)
    input("Press enter to proceed to Step 6...")
    
    print("Step 6: Alice and Bob delete all of their corresponding qubits for which the bases disagree")
    step6()
    print("Alice's sifted key and bases:")
    #print(Alice['siftedBits'])
    #print(Alice['siftedBases'])
    print("Bob's sifted key and bases:")
    #print(Bob['siftedBits'])
    #print(Bob['siftedBases'])
    print("Length of sifted raw key: ", len(Alice['siftedBits']))
    print("Percentage of reduction: ", (BITSIZE-len(Alice['siftedBits']))/BITSIZE*100,"%")
    input("Press enter to proceed to Step 7...")
    
    '''
    print("Step 7: Alice and Bob agree on a small subset of the sifted raw key to publicly reveal")
    print("Note: This is to calculate the quantum bit error rate.")
    input("Press enter to proceed to Step 8...")
    
    print("Step 8: Alice and Bob perform error reconciliation")
    input("Press enter to proceed to Step 9...")
    
    print()"Step 9: Alice and Bob perform primary amplification"
    input("Press enter to exit the program.")
    '''

def quickPresentation():
    print("some stuff")
    
def quickSimulation():
    print("some stuff")


if __name__ == "__main__":
    arg = sys.argv[0]
    #if (arg == '0'):
    done = False
    
    while (not done):
        print("1: Run a detailed presentation (small bit size)")
        print("2: Run a \"quick\" presentation (large bit size)")
        print("3: Quit")
        userInput = input("What would you like to do? ")
        if (userInput == '1'):
            detailedPresentation()
        elif (userInput == '2'):
            quickPresentation()
        elif (userInput == '3'):
            done = True
            
    print("Goodbye!")
        
    #elif (arg == '1'):
        #quickSimulation()