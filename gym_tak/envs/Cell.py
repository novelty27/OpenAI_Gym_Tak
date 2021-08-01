from .Piece import Piece
class Cell:

	CELL_EMPTY = "___"

	def __init__(self, name):
		self.pieces = [Cell.CELL_EMPTY]
		self.name = name
		self._owner = None
		self._placeable = True
		self._stackable = True

	def place(self, piece):
		if (not self.placeable):
			print("Cell not placeable")
			return False
		else:
			self.pieces.append(piece)
			return True

	def add(self, stack):
		if (not self.stackable):
			print("Cell is not stackable")
			return False

		self.pieces = self.pieces + stack
		return True

	def remove(self, height):
		if (height > len(self.pieces)-1):
			print("Requested to remove", str(height), "pieces. Only", str(len(self.pieces) - 1), "in the stack")
			return False
		else:
			stack = self.pieces[-1*height:]
			self.pieces = self.pieces[:-1*height]
			return stack

		print("Unaccounted for condition in cell.remove()")
		return False

	def flatten(self, stack):
		if (self.placeable):
			print("There is nothing in this Cell to flatten")
			return False
		if (self.pieces[-1].type != Piece.PIECE_WALL):
			print("There is no wall to flatten in this Cell")
			return False
		if (len(stack) != 1):
			print("A wall can only be flattened by a capstone on its own")
			return False
		if (stack[0].type != Piece.PIECE_CAPSTONE):
			print("A wall can only be flattened by a capstone")
			return False

		self.pieces[-1].type = Piece.PIECE_STONE
		self.pieces = self.pieces + stack
		return True

	@property
	def owner(self):
		""" Getter for 'owner' """
		if (self.placeable):
			return None
		else:
			return self.pieces[-1].color

	@property
	def placeable(self):
		""" Getter for 'placeable' """
		return (len(self.pieces) == 1)

	@property
	def stackable(self):
		""" Getter for'stackable' """
		if (self.placeable):
			return True
		return self.pieces[-1].stackable

	@property
	def road(self):
		return self.pieces[-1].isRoad

	def __str__(self):
		""" Return the top piece plus a count of how many pieces are in the cell's stack """
		val = str(self.pieces[-1])
		if (len(self.pieces) > 1):
			return val + (str(len(self.pieces)-1))
		else:
			return val