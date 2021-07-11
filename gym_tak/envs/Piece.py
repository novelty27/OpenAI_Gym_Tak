class Piece:

	PIECE_STONE = "stone"
	PIECE_WALL = "wall"
	PIECE_CAPSTONE = "capstone"

	type = PIECE_STONE

	def __init__(self, pieceType=PIECE_STONE, color="?"):
		self.type = pieceType
		self.color = color

	@property
	def color(self):
		""" Getter for 'color' """
		return self._color[0]

	@color.setter
	def color(self, color):
		""" Setter for 'color' """
		self._color = color

	@property
	def type(self):
		""" Getter for 'type' """
		return self._type

	@type.setter
	def type(self, pieceType):
		""" Setter for 'type' """
		self._type = pieceType
		if (pieceType == Piece.PIECE_STONE):
			self.stackable = True
			self.ableToFlatten = False
			self.ableToBeFlattened = False
			self.isRoad = True
		elif (pieceType == Piece.PIECE_WALL):
			self.stackable = False
			self.ableToFlatten = False
			self.ableToBeFlattened = True
			self.isRoad = False
		elif (pieceType == Piece.PIECE_CAPSTONE):
			self.stackable = False
			self.ableToFlatten = True
			self.ableToBeFlattened = False
			self.isRoad = True
		else:
			print("Unaccounted for piece type")
			return False

	def __str__(self):
		return self.color+self.type[0]