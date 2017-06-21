import math

def quadratic (a, b, c):
	disc = math.sqrt(b * b - 4 * a * c)
	return ((-1 * b - disc) / (2 * a), (-1 * b + disc) / (2 * a))

def find_v0 (dict):
	if not ("d" in dict):
		return dict["v"] - dict["a"] * dict["t"]
	elif not ("v" in dict):
		return dict["d"] - 0.5 * dict["a"] * dict["t"] * dict["t"]
	elif not ("t" in dict):
		return math.sqrt(dict["v"] ** 2 - 2 * dict["a"] * dict["d"])
	else:
		return 2 * dict["d"] / dict["t"] - dict["v"]

def find_v (dict):
	if not ("d" in dict):
		return dict["v0"] + dict["a"] * dict["t"]
	elif not ("t" in dict):
		return math.sqrt(dict["v0"] ** 2 + 2 * dict["a"] * dict["d"])
	elif not ("a" in dict):
		return 2 * dict["d"] / dict["t"] - dict["v0"]
	else:
		return dict["d"] / dict["t"] + 0.5 * dict["a"] * dict["t"]

def find_a (dict):
	if not ("d" in dict):
		return (dict["v"] - dict["v0"]) / dict["t"]
	elif not ("v" in dict):
		return 2 * (dict["d"] - dict["v0"] * dict["t"]) / (dict["t"] ** 2)
	elif not ("t" in dict):
		return (dict["v"] ** 2 - dict["v0"] ** 2) / (2 * dict["d"])
	else:
		return 2 * (dict["v"] * dict["t"] - dict["d"]) / (dict["t"] ** 2)

def find_d (dict):
	if not ("v" in dict):
		return dict["v0"] * dict["t"] + 0.5 * dict["a"] * dict["t"] * dict["t"]
	elif not ("t" in dict):
		return (dict["v"] ** 2 - dict["v0"] ** 2) / (2 * dict["a"])
	elif not ("a" in dict):
		return 0.5 * (dict["v"] + dict["v0"]) * dict["t"]
	else:
		return dict["v"] * dict["t"] - 0.5 * dict["a"] * dict["t"] * dict["t"]

def find_t (dict):
	if not ("d" in dict):
		return (dict["v"] - dict["v0"]) / dict["a"]
	elif not ("v" in dict):
		return quadratic(0.5 * dict["a"], dict["v0"], -1 * dict["d"])[1]
	elif not ("a" in dict):
		return (2 * dict["d"]) / (dict["v"] + dict["v0"])
	else:
		return quadratic(0.5 * dict["a"], -1 * dict["v"], dict["d"])[1]
