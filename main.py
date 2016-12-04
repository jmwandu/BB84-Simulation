"""
Joshua Mwandu, Max Taylor II
BB-84 Protocol Simulator
Fall 2016 Mathematics Research Project
4 December, 2016
"""
from random import randint

Alice = {'generatedBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
Bob = {'measuredBits':[], 'chosenBases':[], 'siftedBits':[], 'siftedBases':[]}
Eve = {'measuredBits':[], 'chosenBases':[]}
correct_basis_indeces = []
BITSIZE = 10

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
    
#step 6 of the protocol        
def step6():
    temp_bit_list = []
    temp_basis_list = []
    for i in range(0, BITSIZE):
        if (i in correct_basis_indeces):
            temp_bit_list.append(Alice['generatedBits'][i])
            temp_basis_list.append(Alice['chosenBases'][i])
    
    Alice['siftedBits'] = temp_bit_list
    Bob['siftedBits'] = temp_bit_list
    Alice['siftedBases'] = temp_basis_list
    Bob['siftedBases'] = temp_basis_list

#where all the magic happens
def main():
    done = False
    
    while(not done):
        
        print("Welcome!")
        print("This program will create a secure key using the BB84 Protocol.")
        input("Press enter to proceed to Step 1...")
        
        print("Step 1: Alice prepares a random string of bits and encodes them randomly in either the X or Z bases")
        step1()
        print(Alice)
        input("Press enter to proceed to Step 2...")
        
        print("Step 2: Alice sends each qubit to Bob")
        print("Step 3: Bob randomly measures each qubit in either X or Z bases and records his results")
        step2_3()
        print(Bob)
        input("Press enter to proceed to Step 4...")
        
        print("Step 4: Bob publicly tells Alice what basis he measured each qubit in")
        print("Step 5: Alice tells Bob for which qubits he chose the correct basis")
        step4_5()
        print(correct_basis_indeces)
        input("Press enter to proceed to Step 6...")
        
        print("Step 6: Alice and Bob delete all of their corresponding qubits for which the bases disagree")
        step6()
        print("Alice: ", Alice['siftedBits'], Alice['siftedBases'])
        print("Bob: ", Bob['siftedBits'], Bob['siftedBases'])
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
        
        done = True
        
if __name__ == "__main__":
    main()