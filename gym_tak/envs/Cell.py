class Cell:
	def __init__(self):
		self.pieces = ["__"]

	def place(self, color, piece):
		self.pieces.append(color+piece)
		return True

	def __str__(self):
		return self.pieces[-1]