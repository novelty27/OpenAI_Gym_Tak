from .Piece import Piece

class Player:
	name = "Player"
	stoneCount = 0
	capstoneCount = 0

	def __init__(self, name, color, stones, capstones):
		self.name = name
		self.color = color
		self.stoneCount = stones
		self.capstoneCount = capstones

	def getPiece(self, pieceType):
		if (pieceType == Piece.PIECE_STONE or pieceType == Piece.PIECE_WALL):
			if (self.stoneCount > 0):
				self.stoneCount -= 1
				return Piece(pieceType, self.color)
			else:
				print(self.color, "has no more stones to play")
				return None
		elif (pieceType == Piece.PIECE_CAPSTONE):
			if (self.capstoneCount > 0):
				self.capstoneCount -= 1
				return Piece(pieceType, self.color)
			else:
				print(self.color, "has no more capstones to play")
				return None
		else:
			print("That is not an acceptable piece type. Try stone, wall, or capstone")
			return None