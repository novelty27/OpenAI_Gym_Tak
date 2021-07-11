class Piece:

	PIECE_STONE = "stone"
	PIECE_WALL = "wall"
	PIECE_CAPSTONE = "capstone"

	type = PIECE_STONE

	def __init__(self, pieceType=PIECE_STONE, color="?"):
		self.type = pieceType
		self.color = color
		self.stackable = True
		self.ableToFlatten = False
		self.ableToBeFlattened = False
		if (pieceType == Piece.PIECE_STONE):
			pass
		elif (pieceType == Piece.PIECE_WALL):
			self.stackable = False
			self.ableToBeFlattened = True
		elif (pieceType == Piece.PIECE_CAPSTONE):
			self.stackable = False
			self.ableToFlatten = True
		else:
			print("Unaccounted for piece type")

	@property
	def color(self):
		""" Getter for 'color' """
		return self._color[0]

	@color.setter
	def color(self,value):
		""" Setter for 'color' """
		self._color = value

	@property
	def type(self):
		""" Getter for 'type' """
		return self._type[0]

	@type.setter
	def type(self,value):
		""" Setter for 'type' """
		self._type = value

	def __str__(self):
		return self.color+self.type