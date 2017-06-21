from scipy.spatial import distance
import measurements as m
import kinematics as kn
import room8 as rm
import astar as ast

# lst: list of (distance, velocity) pairings on a graph
def calc_info (lst):
	info = []
	for i in range(len(lst) - 1):
		dst = lst[i+1][0]
		vi, vf = lst[i][1], lst[i+1][1]
		time = (2*dst)/(vi+vf)
		info.append((time, vi, vf, dst))
	return info

# takes two lists of numbers and returns a list of pairs
def zip_lst (lst1, lst2):
	if not len(lst1) == len(lst2):
		print("lists not same length")
	zipped = []
	for i in range(len(lst1)):
		zipped.append((lst1[i], lst2[i]))
	return zipped

# gets rid of continues in path
def shorten (lst):
	shortened = [lst[0]]
	for i in range(1, len(lst) - 1):
		loc1, loc2, loc3 = lst[i-1], lst[i], lst[i+1]
		if not ast.collinear (loc1, loc2, loc3):
			shortened.append(lst[i])
	shortened.append(lst[len(lst)-1])
	return shortened

# gets distances between the points in lst
def get_lengths (lst):
	lengths = []
	for i in range(len(lst)-1):
		lengths.append(distance.euclidean(lst[i], lst[i+1]))
	return lengths

# the first part of the trip
def first (dst, d, v, stat):
	if dst > 360.+stat["d_ca"]+stat["tr"]:
		d = d + [360., dst-360.-stat["d_ca"]-stat["tr"], stat["d_ca"], stat["tr"]]
		v = v + [stat["v_a"], stat["v_a"], stat["v_c"], stat["v_c"]]
	elif dst > stat["tr"]+stat["d_0c"]:
		d1 = (stat["v_c"]*stat["v_c"] + 2*stat["a"]*(dst-stat["tr"]))/(4*stat["a"])
		d2 = dst-d1-stat["tr"]
		new_v = kn.find_v({"v0": 0., "a": stat["a"], "d": d1})
		d = d + [d1, d2, stat["tr"]]
		v = v + [new_v, stat["v_c"], stat["v_c"]]
	elif dst > stat["d_0c"]:
		d = d + [stat["d_0c"], dst-stat["d_0c"]]
		v = v + [stat["v_c"], stat["v_c"]]
	else:
		new_v = kn.find_v({"v0": 0., "a": stat["a"], "d": dst})
		d = d + [dst]
		v = v + [new_v]
	return (d, v)

# all middle parts of the trip
def middle (lengths, d, v, stat):
	for i in range(1, len(lengths)-1):
		dst = lengths[i]
		if dst > 2*(stat["d_ca"]+2*stat["tr"]):
			d = d + [stat["tr"], stat["d_ca"], dst-2*(stat["d_ca"]+stat["tr"]), stat["d_ca"], stat["tr"]]
			v = v + [stat["v_c"], stat["v_a"], stat["v_a"], stat["v_c"], stat["v_c"]]
		elif dst > 2*stat["tr"]:
			dst2 = (dst-2*stat["tr"])/2
			new_v = kn.find_v({"v0": stat["v_c"], "a": stat["a"], "d": dst2})
			d = d + [stat["tr"], dst2, dst2, stat["tr"]]
			v = v + [stat["v_c"], new_v, stat["v_c"], stat["v_c"]]
		else:
			d = d + [dst]
			v = v + [stat["v_c"]]
	return (d, v)

# the last part of the trip
def last (dst, d, v, stat):
	if dst > stat["tr"]+stat["d_ca"]+360.:
		d = d + [stat["tr"], stat["d_ca"], dst-stat["tr"]-stat["d_ca"]-360., 360.]
		v = v + [stat["v_c"], stat["v_a"], stat["v_a"], 0.]
	elif dst > stat["tr"]+stat["d_0c"]:
		d2 = (stat["v_c"]*stat["v_c"] + 2*stat["a"]*(dst-stat["tr"]))/(4*stat["a"])
		d1 = dst-d2-stat["tr"]
		new_v = kn.find_v({"v0": stat["v_c"], "a": stat["a"], "d": d1})
		d = d + [stat["tr"], d1, d2]
		v = v + [stat["v_c"], new_v, 0.]
	elif dst > stat["d_0c"]:
		d = d + [dst-stat["d_0c"], stat["d_0c"]]
		v = v + [stat["v_c"], 0.]
	else:
		d = d + [dst]
		v = v + [0.]
	return (d, v)

# if lengths == 1 in the first part of the trip
def first_straight (dst, d, v, stat):
	if dst > 360.:
		d = d + [dst-360., 360.]
		v = v + [stat["v_a"], 0.]
	else:
		print("Please enter door slowly.")
		new_v = kn.find_v({"v0": 0., "a": stat["a"], "d": dst})
		d = d + [dst]
		v = [new_v, 0.] 
	return (d, v)

# first length in the first part of the trip
def first_start (dst, d, v, stat):
	if dst > stat["d_ca"]+stat["tr"]:
		d = d + [dst-stat["d_ca"]-stat["tr"], stat["d_ca"], stat["tr"]]
		v = v + [stat["v_a"], stat["v_c"], stat["v_c"]]
	elif dst > stat["d_ca"]:
		d = d + [dst-stat["d_ca"], stat["d_ca"]]
		v = v + [stat["v_a"], stat["v_c"]]
	else:
		print("Please enter door slowly.")
		d = d + [dst]
		new_v = kn.find_v({"v0": stat["v_c"], "a": stat["a"], "d": dst})
		v = [new_v, stat["v_c"]]
	return (d, v)

# if lengths == 1 in the middle of the trip
def middle_straight (dst, d, v, stat): 
	if dst > 2*360.:
		d = d + [360., dst-2*360., 360.]
		v = v + [stat["v_a"], stat["v_a"], 0.]
	else:
		dst2 = dst/2
		new_v = kn.find_v({"v0": 0., "a": stat["a"], "d": dst2})
		d = d + [dst2, dst2]
		v = v + [new_v, 0.]
	return (d, v)

# if lengths == 1 in the last part of the trip
def last_straight (dst, d, v, stat):
	if dst > 360.:
		d = d + [360., dst-360.]
		v = v + [stat["v_a"], stat["v_a"]]
	else:
		new_v = kn.find_v({"v0": 0., "a": stat["a"], "d": dst})
		d = d + [dst]
		v = v + [new_v]
	return (d, v)

# last length in the last part of the trip
def last_end (dst, d, v, stat):
	if dst > stat["tr"]+stat["d_ca"]:
		d = d + [stat["tr"], stat["d_ca"], dst-stat["tr"]-stat["d_ca"]]
		v = v + [stat["v_c"], stat["v_a"], stat["v_a"]]
	elif dst > stat["tr"]:
		new_v = kn.find_v({"v0": stat["v_c"], "a": stat["a"], "d": dst-stat["tr"]})
		d = d + [stat["tr"], dst-stat["tr"]]
		v = v + [stat["v_c"], new_v]
	else:
		d = d + [dst]
		v = v + [stat["v_c"]]
	return (d, v)

# labels: list of paths
# f: forklift
def time (labels, lst, stats, f):
	graph_info, fklift = [], []

	# door to door
	if len(labels) == 1:
		label = labels[0]
		if f.get_load() > 0: stat = stats["rl"]
		else: stat = stats["nl"]

		for j in range(len(label)):
			coords.append (rm.nodes8[label[j]])

		lengths = get_lengths (shorten (coords))
		if len(lengths) == 1:
			graph_info.append (calc_info ([0, stat["v_a"]], [lengths[0], stat["v_a"]]))
		else:
			init_d, init_v = [0.], [stat["v_a"]]
			(first_d, first_v) = first_start (lengths[0], init_d, init_v, stat)
			(middle_d, middle_v) = middle (lengths, first_d, first_v, stat)
			(d, v) = last_end (lengths[len(lengths)-1], middle_d, middle_v, stat)
			graph_info.append (calc_info (zip_lst(d, v)))
			return (graph_info, [])

	for i in range(len(labels)-1):
		label = labels[i]
		
		if f.get_load() > 0: stat = stats["rl"]
		else: stat = stats["nl"]

		coords = []
		for j in range(len(label)):
			coords.append (rm.nodes8[label[j]])
		lengths = get_lengths (shorten (coords))

		if i == 0:
			init_d, init_v = [0.], [stat["v_a"]]
			if len(lengths) == 1:
				(d, v) = first_straight (lengths[0], init_d, init_v, stat)
			else:
				(first_d, first_v) = first_start (lengths[0], init_d, init_v, stat)
				(middle_d, middle_v) = middle (lengths, first_d, first_v, stat)
				(d, v) = last (lengths[len(lengths)-1], middle_d, middle_v, stat)
		else:
			init_d, init_v = [0.], [0.]
			if len(lengths) == 1:
				(d, v) = middle_straight (lengths[0], init_d, init_v, stat)
			else:
				(first_d, first_v) = first (lengths[0], init_d, init_v, stat)
				(middle_d, middle_v) = middle (lengths, first_d, first_v, stat)
				(d, v) = last (lengths[len(lengths)-1], middle_d, middle_v, stat)
		graph_info = graph_info + calc_info (zip_lst (d, v))

		extra_time = m.frotate*2
		if lst[i+1] > 0: 
			extra_time = extra_time + m.fpick
			f.add_load()
		else: 
			extra_time = extra_time + m.fplace
			f.remove_load()
		graph_info.append ((extra_time, 0, 0, 0))

		height = rm.locs[abs(lst[i+1])]["z"]
		lift = (height-f.get_fkheight())/stat["lift"]
		f.set_fkheight(height)
		if i < len(labels)-2:
			new_height = rm.locs[abs(lst[i+2])]["z"]
			if height > new_height: 
				height = height - new_height
				f.set_fkheight(new_height)
			else:
				height = 0.
		else:
			f.set_fkheight(0.)
		if f.get_load() > 0: lower = height/stats["rl"]["lower"]
		else: lower = height/stats["nl"]["lower"]
		fklift.append((lift, lower))

	# last length
	init_d, init_v = [0.], [0.]
	label = labels[len(labels)-1]
	coords = []
	for j in range(len(label)):
		coords.append (rm.nodes8[label[j]])
	lengths = get_lengths (shorten (coords))
	if len(lengths) == 1:
		(d, v) = last_straight (lengths[0], init_d, init_v, stat)
	else:
		(first_d, first_v) = first (lengths[0], init_d, init_v, stat)
		(middle_d, middle_v) = middle (lengths, first_d, first_v, stat)
		(d, v) = last_end (lengths[len(lengths)-1], middle_d, middle_v, stat)
	graph_info = graph_info + calc_info (zip_lst (d, v))
	return (graph_info, fklift)


