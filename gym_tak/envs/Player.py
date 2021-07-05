from .Piece import Piece

class Player:
	name = "Player"
	stoneCount = 0
	capstoneCount = 0

	def __init__(self, name, color, stones, capstones):
		self.name = name
		self.color = color
		self.stoneCount = capstones
		self.capstoneCount = capstones