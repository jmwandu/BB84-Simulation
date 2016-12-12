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

def graph(x_label, y_label, x_axis, y_axis, scatter = False):
	if scatter:
		plt.plot(x_axis, y_axis, "ro")
	else:
		plt.plot(x_axis, y_axis)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.title(x_label + " vs " + y_label)
	plt.show()

def Display_graph(data):
	while True:

		print("Please enter the kind of plot you would like: \n"
			"0) Raw Sifted Key vs Final Key Length\n"
			"1) Bit Size vs Raw Sifted Key\n"
			"2) Bit Size vs Final Key Length\n"
			"3) Calculated Secure Key Rate vs Actual Secure key Rate\n"
			"4) Bit Size vs Actual Secure key Rate \n"
			"5) Bit Size vs Calculated Secure Key Rate\n"
			"6) Final Key Length vs Actual Secure key Rate \n"
			"7) Final Key Length vs Calculated Secure Key Rate\n"
			"8) QBER Calculated vs QBER Actual\n"
			"9) Bit Size vs QBER Actual\n"
			"10) Bit Size vs QBER Calculated\n"
			"11) stop graphing\n")
		choice = eval(input("Choice: "))
		
		if choice == 0:
			graph( "Raw Sifted Key",  "Final key length", construct_axis(data,0), construct_axis(data,1))
		elif choice == 1: 
			graph( "Bit Size", "Raw Sifted Key", construct_axis(data,0, True), construct_axis(data,0))
			
		elif choice == 2: 
			graph( "Bit Size", "Final Key Length", construct_axis(data,0, True), construct_axis(data,1))
			
		elif choice == 3:
			graph( "Calculated Secure Key Rate", "Actual Secure Key Rate", construct_axis(data,2), construct_axis(data,3), True)
			
		elif choice == 4:
			graph( "Bit Size", "Acutal Secure Key Rate", construct_axis(data,0, True), construct_axis(data,3))
			
		elif choice == 5: 
			graph( "Bit Size","Calculated Secure Key Rate", construct_axis(data,0, True), construct_axis(data,2))
			
		elif choice == 6:
			graph( "Final Key Length", "Actual Secure Key Rate",  construct_axis(data,1), construct_axis(data,3) )
			
		elif choice == 7:
			graph( "Final Key Length", "Calculated Secure Key Rate", construct_axis(data,1), construct_axis(data,2))
			
		elif choice == 8:
			graph("QBER Calculated", "QBER Actual", construct_axis(data,4), construct_axis(data,5), True)

		elif choice == 9:
			graph("Bit Size", "QBER Actual", construct_axis(data,0, True), construct_axis(data,5))
			
		elif choice == 10:
			graph("Bit Size", "QBER Calculated", construct_axis(data,0, True), construct_axis(data,4))

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
