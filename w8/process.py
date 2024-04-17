class Process():
	def __init__(self, x):
		self.v = set([x])

	def values(self):
		return self.v

	def broadcast(self, ps: list['Process'], f: int):
		assert(self not in ps)
		assert(len(ps) >= f)
		responses_count = [0] * len(ps)
		for _ in range(f + 1):
			for idx, p in enumerate(ps):
				v_p = p.values()
				if v_p:
					self.v.update(v_p)
					responses_count[idx] += 1
		can_decide = responses_count.count(f + 1) >= len(ps) - f
		return min(self.v) if can_decide else None
