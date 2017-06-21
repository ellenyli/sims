import main

# converts yes/no input to boolean
def str_to_bool (s):
	if s == "yes": return True
	elif s == "no": return False
	else: "Please enter 'yes' or 'no'."

lst = []
lst.append(int(input("Door of entry: ")))
while(True):
	node = int(input("Next pallet ID or door of exit: "))
	if node < 1000:
		lst.append(node)
		break
	action = input("Enter 'pick up' or 'drop off': ")
	if action == 'pick up': lst.append(node)
	elif action == 'drop off': lst.append(node * -1)
	else: print("Please enter 'pick up' or 'drop off'.")

plot1 = str_to_bool(input("Graph room (yes/no)? "))
plot2 = str_to_bool(input("Graph time versus velocity (yes/no)? "))
plot3 = str_to_bool(input("Graph distance versus velocity (yes/no)? "))
action = str_to_bool(input("Write to output.csv (yes/no)? "))
model = input("Forklift model: ")

main.path(lst, plot1, plot2, plot3, action, model)
