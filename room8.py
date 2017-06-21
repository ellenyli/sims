import networkx as nx
from scipy.spatial import distance
import data
import graph
import matplotlib.pyplot as plt

# positions
bottom = 0.
top = 4233.
left = 0.
right = 1030.
a1 = 139.5  # horizontal
a2 = 853.3  # vertical
a3 = 525.5  # vertical
a4 = 190.85  # vertical
a5 = 4045.25  # horizontal
d1 = 939.2  # bottom
d4 = 277.  # top

# nodes in room
door1ent = (d1, a1)  # 0
door1 = (d1, bottom)  # 1
door2 = (right, a1)  # 2
door3 = (right, a5)  # 3
door4 = (d4, top)  # 4
door4ent = (d4, a5)  # 5
a4near = (a4, a1)  # 6
a4far = (a4, a5)  # 7
a3near = (a3, a1)  # 8
a3far = (a3, a5)  # 9
a2near = (a2, a1)  # 10
a2far = (a2, a5)  # 11

# list of nodes in room
nodes8 = [door1ent, door1, door2, door3, door4, door4ent, a4near, a4far, a3near, a3far, a2near, a2far]

# list of nodes, including name
info8 = []
info8.append({"name": "door1ent", "loc": door1ent})
info8.append({"name": "door1", "loc": door1, "dir": 90})
info8.append({"name": "door2", "loc": door2, "dir": 180})
info8.append({"name": "door3", "loc": door3, "dir": 180})
info8.append({"name": "door4", "loc": door4, "dir": 270})
info8.append({"name": "door4ent", "loc": door4ent})
info8.append({"name": "a4near", "loc": a4near})
info8.append({"name": "a4far", "loc": a4far})
info8.append({"name": "a3near", "loc": a3near})
info8.append({"name": "a3far", "loc": a3far})
info8.append({"name": "a2near", "loc": a2near})
info8.append({"name": "a2far", "loc": a2far})

# creating graph of room

def eucl (x, y):
	return distance.euclidean(nodes8[x], nodes8[y])

room8 = nx.Graph()
room8.add_edge(0, 1, weight=eucl(0, 1))
room8.add_edge(0, 2, weight=eucl(0, 2))
room8.add_edge(0, 10, weight=eucl(0, 10))
room8.add_edge(6, 8, weight=eucl(6, 8))
room8.add_edge(8, 10, weight=eucl(8, 10))
room8.add_edge(6, 7, weight=eucl(6, 7))
room8.add_edge(8, 9, weight=eucl(8, 9))
room8.add_edge(10, 11, weight=eucl(10, 11))
room8.add_edge(3, 11, weight=eucl(3, 11))
room8.add_edge(5, 7, weight=eucl(5, 7))
room8.add_edge(5, 9, weight=eucl(5, 9))
room8.add_edge(9, 11, weight=eucl(9, 11))
room8.add_edge(4, 5, weight=eucl(4, 5))

# reading in csv file
(locs, ids) = data.list_to_dict(data.read_to_float('Room8/Locations.csv'))

# stripping Z direction from locs
locsxy = data.removeZ(locs)

# adds location to list of nodes
# if num is a pallet id, appends location to nodes and adds appropriate edges
# if num is a node in the room, just returns the index
def add_loc (num):
	num = abs(num)
	if num > 10000000:
		n = (num//10) * 10 + 1
		index = len(nodes8)
		loc = (locs[n]["x"], locs[n]["y"])
		aisle, bay = (num // 10000) % 1000, (num % 10000) // 10
		if aisle == 1:
			nodes8.append((loc[0], nodes8[6][1]))
			if bay <= 6:
				room8.add_edge(8, index, weight=loc[0]-nodes8[8][0])
				room8.add_edge(10, index, weight=nodes8[10][0]-loc[0])
			elif bay <= 13:
				room8.add_edge(6, index, weight=loc[0]-nodes8[6][0])
				room8.add_edge(8, index, weight=nodes8[8][0]-loc[0])
			else:
				room8.add_edge(6, index, weight=nodes8[6][0]-loc[0])

		elif aisle == 2:
			nodes8.append((nodes8[10][0], loc[1]))
			room8.add_edge(10, index, weight=eucl(10, index))
			room8.add_edge(11, index, weight=eucl(11,index))
		elif aisle == 3:
			nodes8.append((nodes8[8][0], loc[1]))
			room8.add_edge(8, index, weight=eucl(8, index))
			room8.add_edge(9, index, weight=eucl(9,index))
		elif aisle == 4:
			nodes8.append((nodes8[6][0], loc[1]))
			room8.add_edge(6, index, weight=eucl(6, index))
			room8.add_edge(7, index, weight=eucl(7,index))
		else:
			nodes8.append((loc[0], nodes8[7][1]))
			if bay <= 3:
				room8.add_edge(3, index, weight=loc[0]-nodes8[3][0])
				room8.add_edge(11, index, weight=nodes8[11][0]-loc[0])
			elif bay <= 9:
				room8.add_edge(11, index, weight=loc[0]-nodes8[11][0])
				room8.add_edge(9, index, weight=nodes8[9][0]-loc[0])
			elif bay <= 13:
				room8.add_edge(9, index, weight=loc[0]-nodes8[9][0])
				room8.add_edge(5, index, weight=nodes8[5][0]-loc[0])
			elif bay <= 14:
				room8.add_edge(5, index, weight=loc[0]-nodes8[5][0])
				room8.add_edge(7, index, weight=nodes8[7][0]-loc[0])
			else:
				room8.add_edge(7, index, weight=nodes8[7][0]-loc[0])
		info8.append({"name": num, "loc": room8[index]})
		return index
	else:
		loc = nodes8[num]
		return num

def plot_room():
	plt.plot([0, 840], [71, 71], 'k--')
	plt.plot([840, 840], [0, 71], 'k--')
	plt.plot([116, 116], [208, 3972], 'k--')
	plt.plot([0, 116], [208, 208], 'k--')
	plt.plot([0, 116], [3972, 3972], 'k--')
	plt.plot([58, 58], [208, 3972], 'k--',c='0.5')
	plt.plot([263, 263], [208, 3972], 'k--')
	plt.plot([312, 312], [208, 3972], 'k--',c='0.5')
	plt.plot([361, 361], [208, 3972], 'k--')
	plt.plot([410, 410], [208, 3972], 'k--',c='0.5')
	plt.plot([459, 459], [208, 3972], 'k--')
	plt.plot([263, 459], [208, 208], 'k--')
	plt.plot([263, 459], [3972, 3972], 'k--')
	plt.plot([595, 595], [208, 3972], 'k--')
	plt.plot([643.5, 643.5], [208, 3972], 'k--',c='0.5')
	plt.plot([692, 692], [208, 3972], 'k--')
	plt.plot([740.5, 740.5], [208, 3972], 'k--',c='0.5')
	plt.plot([789, 789], [208, 3972], 'k--')
	plt.plot([595, 789], [208, 208], 'k--')
	plt.plot([595, 789], [3972, 3972], 'k--')
	plt.plot([0, 243], [4121, 4121], 'k--')
	plt.plot([316, 1030], [4121, 4121], 'k--')
	plt.plot([243, 243], [4121, 4233], 'k--')
	plt.plot([316, 316], [4121, 4233], 'k--')
	plt.plot([919, 1030], [208, 208], 'k--')
	plt.plot([919, 919], [208, 3817], 'k--')
	plt.plot([919, 985], [3817, 3817], 'k--')
	plt.plot([975, 975], [3817, 3996], 'k--')
	plt.plot([975, 1030], [3996, 3996], 'k--')
	plt.plot([975, 975], [208, 3972], 'k--',c='0.5')
	plt.plot([0, 1030], [4177, 4177], 'k--',c='0.5')
	plt.plot([0, 1030], [0, 0], 'k-', lw = 2)
	plt.plot([0, 1030], [4233, 4233], 'k-', lw = 2)
	plt.plot([0, 0], [0, 4233], 'k-', lw = 2)
	plt.plot([1030, 1030], [0, 4233], 'k-', lw = 2)

def plot_pallets():
	# plotting pallets
	a1, a2l, a2r, a3l, a3r, a4l, a4r, a5 = [], [], [], [], [], [], [], []
	for item in locsxy:
		aisle, bay = (item // 10000) % 1000, (item % 10000) // 10
		if aisle == 1: a1.append((locsxy[item]["x"], locsxy[item]["y"]))
		elif aisle == 2 and bay % 2 == 0: a2l.append((locsxy[item]["x"], locsxy[item]["y"]))
		elif aisle == 2 and bay % 2 == 1: a2r.append((locsxy[item]["x"], locsxy[item]["y"]))
		elif aisle == 3 and bay % 2 == 0: a3l.append((locsxy[item]["x"], locsxy[item]["y"]))
		elif aisle == 3 and bay % 2 == 1: a3r.append((locsxy[item]["x"], locsxy[item]["y"]))
		elif aisle == 4 and bay % 2 == 0: a4l.append((locsxy[item]["x"], locsxy[item]["y"]))
		elif aisle == 4 and bay % 2 == 1: a4r.append((locsxy[item]["x"], locsxy[item]["y"]))
		else: a5.append((locsxy[item]["x"], locsxy[item]["y"]))
	a1.reverse()
	a5.reverse()

	# getting dimensions of pallets in each aisle
	aisles = [a1, a4l, a4r, a3l, a3r, a2l, a2r[:63], a2r[63:], a5[:4], a5[4:]]
	dims = []
	dims.append(graph.plot_aisle_bottom (a1, 0))
	dims.append(graph.plot_aisle_left (a4l, 0))
	dims.append(graph.plot_aisle_right (a4r, 361))
	dims.append(graph.plot_aisle_left (a3l, 361))
	dims.append(graph.plot_aisle_right (a3r, 692))
	dims.append(graph.plot_aisle_left (a2l, 692))
	dims.append(graph.plot_aisle_right (a2r[:63], 1030))
	dims.append(graph.plot_aisle_right (a2r[63:], 1030))
	dims.append(graph.plot_aisle_top (a5[:4], 4233))
	dims.append(graph.plot_aisle_top (a5[4:], 4233))

	return (aisles, dims)

def plot_nodes(labels, sub, lst):
	# plotting nodes
	x, y = [], []
	for item in nodes8:
		x.append(item[0])
		y.append(item[1])
	for i in range(len(x)):
		plt.plot(x[i], y[i], 'o', ms=3, color='0')

	# displaying labels
	for i in range(len(labels)):
		label = labels[i]
		plt.annotate("p{}".format(i+1), (x[label[0]], y[label[0]]))
		if i == len(labels) - 1:
			plt.annotate("p{}".format(i+2), (x[label[len(label)-1]], y[label[len(label)-1]]))
		for j in range(1, len(label)-1):
			plt.annotate("{}".format(label[j]), (x[label[j]], y[label[j]]))

	plt.suptitle("Path: \n{} p{} ".format(sub, len(lst)), fontsize=10, fontweight='bold')

	return (x, y)
