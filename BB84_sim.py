import BB84
import pickle
import matplotlib.pyplot as plt

def simulate(bit_size, iterations):
	return [BB84.quickSimulation(bit_size) for i in range(iterations)]

def build_dataset():
	min_bit_size = eval(input("Please enter the min bit size you would like to simulate: "))
	max_bit_size = eval(input("Please enter the max bit size you would like to simulate: "))
	increment = eval(input("Please enter the increment bit size you would like to simulate: "))
	iterations = eval(input("Please enter the number of iterations you would like to simulate: "))
	return [(bit_value, simulate(bit_value, iterations)) for bit_value in range(min_bit_size, (max_bit_size+1), increment)]
	
def record_to_file(file_name, data):
	data_file = open(file_name, 'wb')
	pickle.dump(data, data_file)
	data_file.close()

def load_data(file_name):
	data_file = open(file_name, 'rb')
	data = pickle.load(data_file)
	data_file.close()
	return data


def construct_axis(data, index, bit=False):
	if bit:
		return [data[row][0] for row in range(len(data))]
	axis= []
	for row in range(len(data)):
		total = 0
		for col in range(len(data[row][1])):
			total += data[row][1][col][index]
		axis.append(total/ len(data[row][1]))
	return axis

def graph(x_label, y_label, x_axis, y_axis):
	print(y_axis)
	plt.plot(x_axis, y_axis, "ro-")
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.show()

def Display_graph(data):
	print(data[0][1])
	while True:

		print("Please enter the kind of plot you would like: \n"
			"0) Raw Sifted Key vs Final key length\n"
			"1) Bit size vs Raw Sifted Key\n"
			"2) Bit size vs Final key length\n"
			"3) Calculated QBER vs Actual QBER\n"
			"4) Bit size vs Acutal QBER \n"
			"5) Bit size vs Calculated QBER\n"
			"6) Final key length vs Actual QBER \n"
			"7) Final key length vs Calculated QBER\n"
			"8) stop graphing\n")
		choice = eval(input("Choice: "))
		
		if choice == 0:
			graph( "Raw Sifted Key",  "Final key length", construct_axis(data,0), construct_axis(data,1))
		elif choice == 1: 
			graph( "Bit size", "Raw Sifted Key", construct_axis(data,0, True), construct_axis(data,0))
			
		elif choice == 2: 
			graph( "Bit size", "Final key length", construct_axis(data,0, True), construct_axis(data,1))
			
		elif choice == 3:
			graph( "Calculated secure key rate", "Actual secure key rate", construct_axis(data,2), construct_axis(data,3))
			
		elif choice == 4:
			graph( "Bit size", "Acutal secure key rate", construct_axis(data,0, True), construct_axis(data,3))
			
		elif choice == 5: 
			graph( "Bit size","Calculated secure key rate", construct_axis(data,0, True), construct_axis(data,2))
			
		elif choice == 6:
			graph( "Final key length", "Actual secure key rate",  construct_axis(data,1), construct_axis(data,3) )
			
		elif choice == 7:
			graph( "Final key length", "Calculated secure key rate", construct_axis(data,1), construct_axis(data,2))
			
		elif choice == 8:
			graph("QBER Calculated", "QBER Actual", construct_axis(data,4), construct_axis(data,5))

		elif choice == 9:
			graph("Bit size", "QBER size", construct_axis(data,0, True), construct_axis(data,5))
			
		elif choice == 10:
			graph("Bit size", "QBER Calculated", construct_axis(data,0, True), construct_axis(data,4))

		elif choice == 11:
			break

	
def main():
	print("would you like to do: \n"
		"1) Run a simulation \n"
		"2) Plot a simulation \n"
		"3 exit \n")
	choice = eval(input("Choice: "))

	if choice == 1:
		data = build_dataset()
		record_to_file("bit_1000.pkl", data)
	elif choice == 2:
		data = load_data("bit_1000.pkl")
		Display_graph(data)
	elif choice == 3:
		exit()
main()