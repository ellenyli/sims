import room8 as rm
import astar as ast
import matplotlib.pyplot as plt
import graph
import time_path
import measurements as m
import forklift as fk
import data
import kinematics as kn
import csv

fk_data = data.fk_read("Forklifts.csv")

# takes a list of distances and returns cumulative up to that point
# ex. [a, b, c] -> [a, a+b, a+b+c]
def cumulative (lst):
	dst = [0]
	total = 0
	for i in range(len(lst)):
		dst.append(total + lst[i])
		total = total + lst[i]
	return dst

# calculates how many pallets a forklift is carrying
def calc_load (lst):
	counter = 0
	for i in range(1, len(lst)-1):
		if lst[i] > 0: counter = counter + 1
	return counter

# finds path between two points
# start, end: either pallet id's or nodes in room
def find_path (start, end):
	ind_s, ind_e = rm.add_loc (start), rm.add_loc (end)
	return ast.reconstruct_path ((ast.astar (ind_s, ind_e, rm.room8, rm.nodes8))[0], ind_s, ind_e)

def tuple_to_string (p):
	(x, y) = p
	return "(" + str(x) + ", " + str(y) + ")"

def display (time, distance, lst, load, fork):
	result = []
	index = 0
	for i in range(len(time)-1):
		row1, row2 = [], []
		t1, t2 = time[i], time[i+1]
		dst1, dst2 = distance[i], distance[i+1]
		if dst1 == dst2:
			node = lst[index+1]
			if node > 0: 
				row1.append('traveling to pick up')
				row2.append('picking up pallet')
			else: 
				row1.append('traveling to drop off')
				row2.append('dropping off pallet')
			row1 = row1 + [str(d1), str(graph.dec2(t1)), rm.nodes8[abs(node)], load[index]]
			row2 = row2 + [str(d2), str(graph.dec2(t2)), rm.nodes8[abs(node)], load[]]
			index = index + 1
			result = result + [row1, row2]

	return (t_short, d_short)

# finds path connecting each item in lst
# plots room and pallets, as well as paths and their labels
def path (lst, plot1, plot2, plot3, action, model):
	# f = fk.forklift(m.avg_v, m.dst, m.corner_t, m.tr)
	fd = fk_data[model]
	load = calc_load(lst)
	f = fk.forklift(fd["tr"], fd["lift"], fd["v_nl"], fd["v_rl"], fd["lift_nl"], fd["lift_rl"], fd["lower_nl"], fd["lower_rl"], load, 0)

	# forklift info
	tr = f.tr()
	lift = f.lift()
	v_nl = f.v_nl()
	v_rl = f.v_rl()
	a_nl = f.a_nl()
	a_rl = f.a_rl()
	v_cnl = f.v_cnl()
	v_crl = f.v_crl()
	lift_nl = f.lift_nl()
	lift_rl = f.lift_rl()
	lower_nl = f.lower_nl()
	lower_rl = f.lower_rl()
	stat = {"nl": {"tr": tr, "lift": lift, "v_a": v_nl, "a": a_nl, "v_c": v_cnl, "d_0c": kn.find_d({"v0": 0., "v": v_cnl, "a": a_nl}), "d_ca": kn.find_d({"v0": v_cnl, "v": v_nl, "a": a_nl}), "lift": lift_nl, "lower": lower_nl},
			"rl": {"tr": tr, "lift": lift, "v_a": v_rl, "a": a_rl, "v_c": v_crl, "d_0c": kn.find_d({"v0": 0., "v": v_crl, "a": a_rl}), "d_ca": kn.find_d({"v0": v_crl, "v": v_rl, "a": a_rl}), "lift": lift_rl, "lower": lower_rl}}

	# sub: string for the subtitle
	# labels: labels to display
	sub = ""
	labels = []
	for i in range(len(lst)-1):
		p = find_path(lst[i], lst[i+1])
		sub = sub + " p{} {}".format(i+1, p[1:len(p)-1])
		labels.append(p)

	# room plot
	if plot1:
		graph.graph_1 (labels, sub, lst)

	(info1, info2, load_data, fork_data) = time_path.time(labels, lst, stat, f)
	t, d = [], []
	for i in range(len(info1)):
		t.append(info1[i][0])
		d.append(info1[i][3])
	t_cum = cumulative (t)
	d_cum = cumulative (d)
	print("t {}".format(t))
	print()
	print("d {}".format(d))
	print()
	print("t_cum {}".format(t_cum))
	print()
	print("d_cum {}".format(d_cum))

	# time versus velocity plot
	if plot2:
		graph.graph_t (info1, info2, t_cum)

	# distance versus velocity plot
	if plot3:
		graph.graph_d (info1, d_cum)

	if action:
		# displaying a file of actions
		output = []
		file = csv.writer(open("output.csv", "w"))
		file.writerow(['Action', 'Distance', 'End Time', 'End Loc', 'Load', 'Fork Height'])
		file.writerow(['initial', 0, tuple_to_string(rm.nodes8[lst[0]]), str(load), str(0)])
		disp = display (t_cum, d_cum, lst, load_data, fork_data)
		for i in range(1, len(lst)-1):
			line = []
			file.writerow(line)
		file.writerow(['exit', 'hi',tuple_to_string(rm.nodes8[lst[len(lst)-1]]), str(f.get_load()), str(f.get_fkheight())])

	# if user requested a plot
	if plot1 or plot2 or plot3:
		plt.show()
