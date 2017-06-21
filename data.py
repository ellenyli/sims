import csv

# takes a csv file and reads it as a 2-D array of floats
def read_to_float (s):
	with open(s) as file:
		reader = csv.reader(file, delimiter=",")
		data = list(reader)

	for row in range(len(data)):
		for col in range(len(data[row])):
			data[row][col] = float(data[row][col])

	return data

# takes a 2-D array and returns a dict, with key equal to pallet id
def list_to_dict (data):
	dict1, dict2 = {}, {}
	for row in data:
		dict1[row[4]] = {'x': row[0], 
						'y': row[1], 
						'z': row[2], 
						'depth': row[3], 
						'height': row[5]}
		dict2[(row[0], row[1])] = row[4]

	return (dict1, dict2)

# data: a dict
def removeZ (data):
	# deletes z-direction
	rem = {}
	for item in data:
		if item % 10 == 1:
			rem[item] = data[item]
	return rem

def fk_read (s):
	with open(s) as file:
		reader = csv.reader(file, delimiter=",")
		data = list(reader)

	for row in range(len(data)):
		for col in range(1, len(data[row])):
			data[row][col] = float(data[row][col])

	dict = {}
	for row in data:
		dict[row[0]] = {"tr": row[1], 
						"lift": row[2], 
						"v_nl": row[3], 
						"v_rl": row[4],
						"lift_nl": row[5],
						"lift_rl": row[6],
						"lower_nl": row[7],
						"lower_rl": row[8]}

	return dict