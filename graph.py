import matplotlib.pyplot as plt
import matplotlib.patches as patches
import room8 as rm
import measurements as m

# positive slope: green
# constant velocity: blue
# negative slope: red
def color_line (p1, p2):
	(x1, y1), (x2, y2) = p1, p2
	slope = (y2-y1)/(x2-x1)
	if slope > 0: return 'g'
	elif slope < 0: return 'r'
	elif y1 == 0: return 'orange'
	else: return 'b'

def text_pos (p):
	(x, y) = p
	if y > 65: return (5, 50)
	return (-50, -10)

# rounds to two decimals
def dec2 (n):
	return round(n, 2)

# plots a rectangle of width w and height h centered around (x,y) with color col
def plot (x, y, w, h, col):
	plt.plot([x-w/2, x-w/2], [y-h/2, y+h/2], 'k-', c=col)
	plt.plot([x+w/2, x+w/2], [y-h/2, y+h/2], 'k-', c=col)
	plt.plot([x-w/2, x+w/2], [y-h/2, y-h/2], 'k-', c=col)
	plt.plot([x-w/2, x+w/2], [y+h/2, y+h/2], 'k-', c=col)

# plots a colored rectangle based on height and displays legend
def plot_color (x, y, w, h, height, figure, index):
	if index > 0: htype = '\\\\\\\\\\'
	else: htype = '//////'
	col = ['m', 'r', 'coral', 'y', 'g', 'b']
	rect = figure.add_subplot (111)
	rect.add_patch(patches.Rectangle((x-w/2,y-h/2),w,h,facecolor=col[height-1],hatch=htype))

# plots pallets in lst on the left of a vertical aisle
# limit: where pallets should end 
def plot_aisle_left (lst, limit):
	w = lst[0][0] - limit
	h = lst[1][1] - lst[0][1]
	for i in range(len(lst)):
		(x, y) = (lst[i][0]-w/2, lst[i][1])
		plot(x, y, w, h, '0.5')
	return (w, h)

# plots pallets in lst on the right of a vertical aisle
# limit: where pallets should end
def plot_aisle_right (lst, limit):
	w = limit - lst[0][0]
	h = lst[1][1] - lst[0][1]
	for i in range(len(lst)):
		(x, y) = (lst[i][0]+w/2, lst[i][1])
		plot (x, y, w, h, '0.5')
	return (w, h)

# plots pallets in lst on the top of a horizontal aisle
# limit: where pallets should end
def plot_aisle_top (lst, limit):
	w = lst[1][0] - lst[0][0]
	h = limit - lst[0][1]
	for i in range(len(lst)):
		(x, y) = (lst[i][0], lst[i][1]+h/2)
		plot (x, y, w, h, '0.5')
	return (w, h)

# plots pallets in lst on the bottom of a horizontal aisle
# limit: where pallets should end
def plot_aisle_bottom (lst, limit):
	w = lst[1][0] - lst[0][0]
	h = lst[0][1] - limit
	for i in range(len(lst)):
		(x, y) = (lst[i][0], lst[i][1]-h/2)
		plot (x, y, w, h, '0.5')
	return (w, h)

# plotting room
def graph_1 (labels, sub, lst):
	fig1 = plt.figure(figsize=(5,15))
	(aisles, dims) = rm.plot_pallets()

	# takes a pallet id and displays a color based on height of pallet
	def color (index):
		abs_index = abs(index)
		if abs_index > 10000000:
			(x, y) = (rm.locs[abs_index]["x"], rm.locs[abs_index]["y"])
			height = abs_index % 10
			a, b = (abs_index // 10000) % 1000, (abs_index % 10000) // 10
			for i in range(len(aisles)):
				if (x, y) in aisles[i]:
					w, h = dims[i]
					if a >= 2 and a <= 4 and b % 2 == 0:
						plot_color(x-w/2, y, w, h, height, fig1, index)
					elif a >= 2 and a <= 4 and b % 2 == 1:
						plot_color(x+w/2, y, w, h, height, fig1, index)
					elif a == 1:
						plot_color(x, y-h/2, w, h, height, fig1, index)
					else:
						plot_color(x, y+h/2, w, h, height, fig1, index)

	# plotting the room
	rm.plot_room()
	# plot nodes
	rm.plot_nodes(labels, sub, lst)

	for i in range(len(labels)):
		item = labels[i]
		if i < len(labels)-1:
			color (lst[i+1])
		for j in range(len(item) - 1):
			x1, y1 = rm.nodes8[item[j]][0], rm.nodes8[item[j]][1]
			x2, y2 = rm.nodes8[item[j+1]][0], rm.nodes8[item[j+1]][1]
			plt.plot([x1, x2], [y1, y2], 'k-', color='c')

	magenta = patches.Patch(color='m', label='height 1')
	red = patches.Patch(color='r', label='height 2')
	coral = patches.Patch(color='coral', label='height 3')
	yellow = patches.Patch(color='y', label='height 4')
	green = patches.Patch(color='g', label='height 5')
	blue = patches.Patch(color='b', label='height 6')
	pickup = patches.Patch(color='1.', hatch='\\\\\\\\\\', label='picking up')
	dropoff = patches.Patch(color='1.', hatch='//////', label='dropping off')
	handle = [magenta, red, coral, yellow, green, blue, pickup, dropoff]
	plt.legend(handles=handle,bbox_to_anchor=(0.5, 1), ncol=4, prop={'size':8}, loc='lower center')

# plotting time versus velocity
def graph_t (info1, info2, t):
	travel = t[len(t)-1]
	total = t[len(t)-1]
	index2 = 0
	plt.figure(figsize=(30,7))

	for i in range(len(info1)):
		x1, x2, y1, y2 = dec2(t[i]), dec2(t[i+1]), dec2(info1[i][1]), dec2(info1[i][2])
		if y1 + y2 == 0:
			travel = travel - (x2 - x1)
			(lift, lower) = info2[index2]
			x1r, x2r = x1+m.frotate, x2-m.frotate
			if lift + lower > 0:
				plt.plot([x1r-lift, x1r], [3, 3], 'k--', c='darkmagenta',lw=2)
				plt.plot([x2r, x2r+lower], [3, 3], 'k--', c='midnightblue', lw=2)
				plt.plot(x1r-lift, 3, 'o', c='darkmagenta')
				plt.plot(x2r+lower, 3, 'o', c='midnightblue')
			index2 = index2 + 1
			if x2r-x1r > 3: color_pp = 'deepskyblue'
			else: color_pp = 'hotpink'
			plt.plot([x1r, x2r], [3, 3], 'k--', c=color_pp)
			plt.plot(x1r, 3, 'o', c=color_pp)
			plt.plot(x2r, 3, 'o', c=color_pp)
		plt.plot([x1, x2], [y1, y2], 'k-', c=color_line((x1, y1), (x2, y2)))
		plt.plot(x1, y1, 'o', c='y')
		text1 = "({},{})".format(x1, y1)
		plt.annotate(text1, (x1, y1), xytext=text_pos((x1, y1)), textcoords='offset points', rotation=45)
		if i == len(info1)-1:
			plt.plot(x2, y2, 'o', c='y')
			text2 = "({},{})".format(x2, y2)
			plt.annotate(text2, (x2, y2), xytext=text_pos((x2, y2)), textcoords='offset points', rotation=45)

	time_display = "Travel Time: {} sec, Total Time: {} sec".format(dec2(travel), dec2(total))

	plt.suptitle(time_display, fontsize=10, fontweight='bold')
	plt.xlabel("Time (sec)") 
	plt.ylabel("Velocity (in/sec)")
	green = patches.Patch(color='g', label='increasing velocity')
	blue = patches.Patch(color='b', label='constant velocity')
	red = patches.Patch(color='r', label='decreasing velocity')
	orange = patches.Patch(color='orange', label='picking up pallet')
	darkmagenta = patches.Patch(color='darkmagenta', label='lifting forks')
	midnightblue = patches.Patch(color='midnightblue', label='lowering forks')
	hotpink = patches.Patch(color='hotpink', label='picking pallet')
	deepskyblue = patches.Patch(color='deepskyblue', label='placing pallet')
	slopes = [green, blue, red, orange, darkmagenta, midnightblue, hotpink, deepskyblue]
	plt.legend(handles=slopes,bbox_to_anchor=(0.5, 1), ncol=4, prop={'size':8}, loc='lower center')
	plt.gca().set_ylim([-30, 170])

# plotting distance versus velocity
def graph_d (info, d):
	plt.figure(figsize=(30,7))

	for i in range(len(info)):
		x1, x2, y1, y2 = dec2(d[i]), dec2(d[i+1]), dec2(info[i][1]), dec2(info[i][2])
		if not x1 == x2:
			plt.plot([x1, x2], [y1, y2], 'k-', c=color_line((x1, y1), (x2, y2)))
			plt.plot(x1, y1, 'o', c='y')
			plt.plot(x2, y2, 'o', c='y')
			text1 = "({},{})".format(x1, y1)
			plt.annotate(text1, (x1, y1), xytext=text_pos((x1, y1)), textcoords='offset points', rotation=45)
			if i == len(info)-1:
				plt.plot(x2, y2, 'o', c='y')
				text2 = "({},{})".format(x2, y2)
				plt.annotate(text2, (x2, y2), xytext=text_pos((x2, y2)), textcoords='offset points', rotation=45)
			if y1 == 0 and y2 == 0:
				travel = travel - (x2 - x1)

	plt.suptitle("Total Distance: {} inches".format(dec2(d[len(d)-1])), fontsize=10, fontweight='bold')
	plt.xlabel("Distance (in)") 
	plt.ylabel("Velocity (in/sec)")
	green = patches.Patch(color='g', label='increasing velocity')
	blue = patches.Patch(color='b', label='constant velocity')
	red = patches.Patch(color='r', label='decreasing velocity')
	slopes = [green, blue, red]
	plt.legend(handles=slopes,bbox_to_anchor=(0.5, 1), ncol=5, prop={'size':8}, loc='lower center')
	plt.gca().set_ylim([-30, 170])


