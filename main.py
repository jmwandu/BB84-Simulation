"""
Joshua Mwandu, Max Taylor II
BB-84 Protocol Simulator
Fall 2016 Mathematics Research Project
4 December, 2016
"""
import sys
from math import ceil, log, sqrt
from random import randint, random, sample
from multiprocessing import Pool

Alice = {'generatedBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[], 'finalKey':[]}
Bob = {'measuredBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[], 'finalKey':[]}
Eve = {'measuredBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
correct_basis_indices = []
BITSIZE = 0
qber_calculated = 0
qber_actual = 0

#reset all data back to blank to prevent memory overflow
def clear_data():
    Alice = {'generatedBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[], 'finalKey':[]}
    Bob = {'measuredBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[], 'finalKey':[]}
    Eve = {'measuredBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
    correct_basis_indices = []

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
            correct_basis_indices.append(i)

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
        if (i in correct_basis_indices):
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
    #calculate qber_calculated
    reveal_size = ceil(sqrt(len(correct_basis_indices)))
    
    #list of random, sorted indices from Alice's generatedBits list
    #number of indices in list is reveal_size
    random_indicies = sorted(sample(range(len(Alice['siftedBits'])), reveal_size))
    
    random_sample_alice = [Alice['siftedBits'][i] for i in random_indicies]
    random_sample_bob = [Bob['siftedBits'][i] for i in random_indicies]
    
    incorrect = 0
    
    for i in range(reveal_size):
        if (random_sample_alice[i] != random_sample_bob[i]):
            incorrect += 1
    
    global qber_calculated
    qber_calculated = incorrect / reveal_size
    
    #calculate qber_actual
    final_bits_alice = []
    final_bits_bob = []
    
    for i in range(len(Alice['siftedBits'])):
        if (i not in random_indicies):
            final_bits_alice.append(Alice['siftedBits'][i])
            final_bits_bob.append(Bob['siftedBits'][i])
    
    Alice['finalKey'] = final_bits_alice
    Bob['finalKey'] = final_bits_bob
    
    incorrect = 0
    
    for i in range(len(final_bits_alice)):
        if (final_bits_alice[i] != final_bits_bob[i]):
            incorrect += 1
    
    global qber_actual
    qber_actual = incorrect / len(final_bits_alice)

#formula for secure key rate
#takes decimal from 0 to 1, returns the secure key rate as a decimal from 0 to 1
def secureKeyRate(x):
    return ((-x)*log(x, 2) - (1-x)*log(1-x, 2))
    
#presentation to show off the process of the simulation
#goes through each step
def detailedPresentation(bit_size):
    global BITSIZE
    BITSIZE = bit_size
    
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
    print("Indices of bits/bases in which Alice and Bob have the same basis:")
    print(correct_basis_indices)
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
    
    print("Step 7: Alice and Bob agree on a small subset of the sifted raw key to publicly reveal in order to calculate the quantum bit error rate.")
    step7()
    print("The calculated QBER is: " + str(100*qber_calculated) + "%")
    print("The actual QBER is: " + str(100*qber_actual) + "%")
    print("The calculated secure key rate is: " + str(100*secureKeyRate(qber_calculated)) + "%")
    print("The actual secure key rate is: " + str(100*secureKeyRate(qber_actual)) + "%")
    input("Press enter to finish this presentation...\n")
    
    '''
    print("Step 8: Alice and Bob perform error reconciliation")
    input("Press enter to proceed to Step 9...\n")
    
    print()"Step 9: Alice and Bob perform primary amplification"
    input("Press enter to exit the program.")
    '''

#presentaion to show off the speed of the simulation on large bit sizes
#only spits out final QBERs
def quickPresentation(bit_size):
    global BITSIZE
    BITSIZE = bit_size
    step1()
    step2_3()
    step4_5()
    step6()
    step7()
    print("The calculated QBER is: " + str(100*qber_calculated) + "%")
    print("The actual QBER is: " + str(100*qber_actual) + "%")
    print("The calculated secure key rate is: " + str(100*secureKeyRate(qber_calculated)) + "%")
    print("The actual secure key rate is: " + str(100*secureKeyRate(qber_actual)) + "%")
    print("Length of final key: ", len(Alice['finalKey']))
    print("Percentage of reduction: " + str((BITSIZE-len(Alice['finalKey']))/BITSIZE*100) + "%")

#quick simulation used to 
def quickSimulation(bit_size):
    global BITSIZE
    BITSIZE = bit_size
    step1()
    step2_3()
    step4_5()
    step6()
    step7()
    
    raw_sifted_key_length = len(Alice['siftedBits'])
    final_key_length = len(Alice['finalKey'])
    calculated_secure_key_rate = secureKeyRate(qber_calculated)
    actual_secure_key_rate = secureKeyRate(qber_actual)
    
    return (raw_sifted_key_length, final_key_length, calculated_secure_key_rate, actual_secure_key_rate)

#begin the program
if __name__ == "__main__":
    arg = sys.argv
    
    if (arg[1] == '0'):
        done = False
        
        while (not done):
            print("1: Run a detailed presentation")
            print("2: Run a quick presentation")
            print("3: Quit")
            userInput = input("What would you like to do? ")
            if (userInput == '1'):
                userInput =  input("What would you like the bit size to be? (Recommended: small)\n")
                detailedPresentation(int(userInput))
            elif (userInput == '2'):
                userInput =  input("What would you like the bit size to be? (Recommended: large)\n")
                quickPresentation(int(userInput))
            elif (userInput == '3'):
                done = True
                
            clear_data()
                
        print("Goodbye!")
        
    elif (arg[1] == '1'):
        quickSimulation(int(arg[2]))