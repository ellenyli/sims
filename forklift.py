import kinematics as kn

class forklift:
	def __init__(self, tr, lift, v_nl, v_rl, lift_nl, lift_rl, lower_nl, lower_rl, load, fkheight):
		# forklift type stats
		self.type = {"tr": tr, # turning radius
					 "lift": lift, # lift height
					 "v_nl": v_nl, # NL velocity
					 "v_rl": v_rl, # RL velocity
					 "a_nl": kn.find_a({"v0": 0., "v": v_nl, "d": 360.}),
					 "a_rl": kn.find_a({"v0": 0., "v": v_rl, "d": 360.}),
					 "lift_nl": lift_nl,
					 "lift_rl": lift_rl,
					 "lower_nl": lower_nl,
					 "lower_rl": lower_rl
					}
		self.load = load # 0, 1, or 2 pallets
		self.fkheight = fkheight

	def tr(self): return self.type["tr"]
	def lift(self): return self.type["lift"]
	def v_nl(self): return self.type["v_nl"]
	def v_rl(self): return self.type["v_rl"]
	def a_nl(self): return self.type["a_nl"]
	def a_rl(self): return self.type["a_rl"]
	def v_cnl(self): return kn.find_v({"v0": self.type["v_nl"], "a": -1*self.type["a_nl"], "d": 360-self.type["tr"]})
	def v_crl(self): return kn.find_v({"v0": self.type["v_rl"], "a": -1*self.type["a_rl"], "d": 360-self.type["tr"]})
	def lift_nl(self): return self.type["lift_nl"]
	def lift_rl(self): return self.type["lift_rl"]
	def lower_nl(self): return self.type["lower_nl"]
	def lower_rl(self): return self.type["lower_rl"]
	def get_load(self): return self.load
	def remove_load(self): self.load = self.load - 1
	def add_load(self): self.load = self.load + 1
	def get_fkheight(self): return self.fkheight
	def set_fkheight(self, h): self.fkheight = h

