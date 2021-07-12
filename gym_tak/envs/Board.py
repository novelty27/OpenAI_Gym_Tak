from .Cell import Cell
from .Piece import Piece

class Board: 

	ACTION_PLACE = "place"
	ACTION_MOVE = "move"
	ACTION_MOVE_END = "move_end"
	ACTION_FLATTEN = "flatten"

	STATE_MOVE_SUCCESSFUL = True
	STATE_MOVE_UNSUCCESSFUL = False
	STATE_MOVE_CONTINUE = "move_continue"

	DIRECTION_UP = "up"
	DIRECTION_DOWN = "down"
	DIRECTION_LEFT = "left"
	DIRECTION_RIGHT = "right"
	DIRECTION_NONE = False

	def __init__(self, gameData):
		self.height = gameData[0]
		self.width = gameData[1]
		self.pieces = gameData[2]
		self.capstones = gameData[3]
		self.carryLimit = self.width
		self.maxHeight = 2 * (self.pieces + self.capstones)
		self.cells = [[Cell() for x in range(self.width)] for y in range(self.height)]
		self.moveState = Board.STATE_MOVE_UNSUCCESSFUL
		self.moveCoordinate = False
		self.moveDirection = Board.DIRECTION_NONE

	def cells(self):
		return self.cells

	def play(self, player, action):
		if (self.moveState == Board.STATE_MOVE_CONTINUE and action[0] == Board.ACTION_PLACE):
			# May want to check directionality here or we can do that in the move/flatten conditional branch
			print("You may only move or flatten while in a move state")
			return False
		elif (self.moveState == Board.STATE_MOVE_CONTINUE):
			# Currently in a move. Don't touch the carryLimit or the board's state
			pass
		else:
			# Not in a move. Make sure board's state and carryLimit are reset
			self.moveState = Board.STATE_MOVE_UNSUCCESSFUL
			self.moveCoordinate = False
			self.moveDirection = Board.DIRECTION_NONE
			self.carryLimit = self.width

		if (action[0] == Board.ACTION_PLACE):
			#adjust human index to 0 based index
			x = action[2]-1
			y = action[3]-1
			if (not self.isIndexInBounds(x, y)):
				print("Index is out of bounds")
				return False

			#Create piece object to give to the cell
			piece = Piece(action[1], player.color)
			self.moveState = self.cells[x][y].place(piece)
			return self.moveState

		elif (action[0] == Board.ACTION_MOVE or action[0] == Board.ACTION_FLATTEN):
			if (self.moveState == Board.STATE_MOVE_CONTINUE):
				if (len(action) != 2):
					print("You are moving. Please pass in two arguments: an action and a stack height")
					return False
				startX, startY = self.moveCoordinate
				endX, endY = self.getCoordinatesOfDirection(startX, startY, self.moveDirection)
				stackHeight = action[1]
			else:
				#grab input parameters and adjust human index to 0 based index
				if (len(action) != 5):
					print("Please pass in 4 arguments: an action, a startX, a startY, a direction, and a stack height")
					return False
				startX = action[1]-1
				startY = action[2]-1
				endX, endY = self.getCoordinatesOfDirection(startX, startY, action[3])
				stackHeight = action[4]

			if (not self.isMoveLegal(player, startX, startY, endX, endY, stackHeight)):
				return False

			# Do the first half of the move operation (removing pieces from a cell)
			stack = self.cells[startX][startY].remove(stackHeight)
			if (not stack):
				print("Move was not successful. Cells are unchanged")
				return False

			# Do the second half of the move/flatten operation (adding pieces to a cell)
			if (action[0] == Board.ACTION_MOVE):
				moveSuccessful = self.cells[endX][endY].add(stack)
			else:
				moveSuccessful = self.cells[endX][endY].flatten(stack)

			#If not successful, put the cells revert the move
			if (not moveSuccessful and stack):
				self.cells[startX][startY].add(stack)
				print("Move was unsuccessful. Returning stack to original cell")
				return False
			elif (moveSuccessful):
				# Move was successful. Decrement the carryLimit for the next step
				self.carryLimit = len(stack)-1
			else:
				print("Move was unsuccessful and no stack was returned")
				return False

			if (self.carryLimit>=1):
				self.moveState = Board.STATE_MOVE_CONTINUE
				self.moveCoordinate = endX, endY
				self.moveDirection = self.getMoveDirection(startX, startY, endX, endY)
			elif (self.carryLimit == 0):
				self.moveState = Board.STATE_MOVE_SUCCESSFUL
			else:
				print("Unaccounted for condition in end of move")

			return self.moveState

		elif (action[0] == Board.ACTION_MOVE_END):
			if (self.moveState == Board.STATE_MOVE_CONTINUE):
				self.moveState = Board.STATE_MOVE_SUCCESSFUL
				return self.moveState
			else:
				print("Cannot end a move if no move is in progress")
				return self.moveState

		else:
			print("Please make a valid move")
			return False

	def isMoveLegal(self, player, startX, startY, endX, endY, stackHeight):
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

		if (stackHeight > self.carryLimit):
			print("You can only move up to", str(self.carryLimit), "pieces at a time")
			return False

		if (not self.isMoveCardinal(startX, startY, endX, endY)):
			print("Move is not cardinal")
			return False

		if (self.moveLength(startX, startY, endX, endY) != 1):
			print("Move length is over 1 (", str(self.moveLength(startX, startY, endX, endY)), ")")
			return False

		return True

	def isIndexInBounds(self, x, y):
		return not (x < 0 or y < 0 or x >= self.width or y >= self.height)

	def isMoveCardinal(self, startX, startY, endX, endY):
		return (startX == endX or startY == endY)

	def moveLength(self, startX, startY, endX, endY):
		xLength = abs(startX-endX)
		yLength = abs(startY-endY)
		return max(xLength, yLength)

	def getMoveDirection(self, startX, startY, endX, endY):
		if (not self.isMoveCardinal(startX, startY, endX, endY)):
			print("That is not a cardinal move")
			return False

		if (startX == endX and startY < endY):
			return Board.DIRECTION_UP
		elif (startX == endX and startY > endY):
			return Board.DIRECTION_DOWN
		elif (startX > endX and startY == endY):
			return Board.DIRECTION_LEFT
		elif (startX < endX and startY == endY):
			return Board.DIRECTION_RIGHT
		else:
			print("Unknown direction. Perhaps you haven't moved")
			return False

	def getCoordinatesOfDirection(self, startX, startY, direction, length=1):
		if (not self.isIndexInBounds(startX, startY)):
			print("Starting coordinates are out of bounds")
			return -1, -1

		if (direction == Board.DIRECTION_UP):
			endX, endY = startX, startY - length
		elif (direction == Board.DIRECTION_DOWN):
			endX, endY = startX, startY + length
		elif (direction == Board.DIRECTION_LEFT):
			endX, endY = startX - length, startY
		elif (direction == Board.DIRECTION_RIGHT):
			endX, endY = startX + length, startY
		else:
			print("Unknown direction for coordinates:",direction)
			endX, endY = -1, -1

		if (not self.isIndexInBounds(endX, endY)):
			print("Ending coordinates are out of bounds")
			return -1, -1
		else:
			return endX, endY

	def __str__(self):
		boardString = ""
		for y in range(self.width):
			for x in range(self.width):
				boardString = boardString + " " + str(self.cells[x][y])
			boardString = boardString + "\n\n"
		return boardString;