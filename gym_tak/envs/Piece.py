class Piece:
	PIECE_STONE = "stone"
	PIECE_WALL = "wall"
	PIECE_CAPSTONE = "capstone"

	type = PIECE_STONE

	def __init__(self, type=PIECE_STONE):
		self.type = type