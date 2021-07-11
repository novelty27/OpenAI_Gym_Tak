from .Cell import Cell
from .Piece import Piece

class Board: 

	ACTION_PLACE = "place"
	ACTION_MOVE = "move"
	ACTION_FLATTEN = "flatten"

	def __init__(self, gameData):
		self.height = gameData[0]
		self.width = gameData[1]
		self.pieces = gameData[2]
		self.capstones = gameData[3]
		self.carryLimit = self.width
		self.maxHeight = 2 * (self.pieces + self.capstones)
		self.cells = [[Cell() for x in range(self.width)] for y in range(self.height)]

	def cells(self):
		return self.cells

	def play(self, player, action):
		if (action[0] == Board.ACTION_PLACE):
			#adjust human index to 0 based index
			x = action[2]-1
			y = action[3]-1
			if (not self.isIndexInBounds(x, y)):
				return False, "Index is out of bounds"

			#Create piece object to give to the cell
			pieceType = action[1]
			color = player.color
			piece = Piece(pieceType, color)
			return self.cells[x][y].place(piece)

		elif (action[0] == Board.ACTION_MOVE):
			#adjust human index to 0 based index
			startX = action[1]-1
			startY = action[2]-1
			endX = action[3]-1
			endY = action[4]-1
			stackHeight = action[5]
			if (not self.isIndexInBounds(startX, startY) or not self.isIndexInBounds(endX, endY)):
				print("Start or end index is out of bounds")
				return False

			if (startX == endX and startY == endY):
				print("A move cannot start and end in the same place")
				return False

			if (len(self.cells[startX][startY].pieces) == 1):
				print("There are no pieces to move from that cell")
				return False

			if (self.cells[startX][startY].owner != player.color[0]):
				print("Player does not own starting stack")
				return False

			if (not self.isMoveLegal(startX, startY, endX, endY)):
				print("This move is either not cardinal or too far")
				return False

			# Do the first half of the move operation
			stack = self.cells[startX][startY].remove(stackHeight)
			if (not stack):
				print("Move was not successful. Cells are unchanged")
				return False

			# Do the second half of the move operation
			moveSuccessful = self.cells[endX][endY].add(stack)

			#If not successful, put the cells revert the move
			if (not moveSuccessful and stack):
				self.cells[startX][startY].add(stack)
				print("Move was unsuccessful. Returning stack to original cell")
				return False

			return True
		elif(action[0] == Board.ACTION_FLATTEN):
			return self.cells[x][y].flatten(color, piece)
		else:
			print("Please make a valid move")
			return False

		return true

	def isIndexInBounds(self, x, y):
		return not (x < 0 or y < 0 or x >= self.width or y >= self.height)

	def isMoveCardinal(self, startX, startY, endX, endY):
		return (startX == endX or startY == endY)

	def moveLength(self, startX, startY, endX, endY):
		xLength = abs(startX-endX)
		yLength = abs(startY-endY)
		return max(xLength, yLength)

	def isMoveLegal(self, startX, startY, endX, endY):
		if (not self.isMoveCardinal(startX, startY, endX, endY)):
			print("Move is not cardinal")
			return False

		moveLength = self.moveLength(startX, startY, endX, endY)
		if (moveLength != 1):
			print("Move length is over 1 (", str(moveLength), ")")
			return False

		return True

	def __str__(self):
		boardString = ""
		for x in range(self.width):
			for y in range(self.width):
				boardString = boardString + " " + str(self.cells[x][y])
			boardString = boardString + "\n\n"
		return boardString;