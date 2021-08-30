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
	LIST_OF_DIRECTIONS = [DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT]
	LIST_OF_OPPOSITE_DIRECTIONS = [DIRECTION_DOWN, DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_LEFT]

	NODE_UP = "up"
	NODE_DOWN = "down"
	NODE_LEFT = "left"
	NODE_RIGHT = "right"
	LIST_OF_NODES = [NODE_UP, NODE_DOWN, NODE_LEFT, NODE_RIGHT]
	LIST_OF_OPPOSITE_NODES = [NODE_DOWN, NODE_UP, NODE_RIGHT, NODE_LEFT]

	def __init__(self, gameData):
		self.height = gameData[0]
		self.width = gameData[1]
		self.pieces = gameData[2]
		self.capstones = gameData[3]
		self.carryLimit = self.width
		self.maxHeight = 2 * (self.pieces + self.capstones)
		self.cells = [[Cell(y * self.width + x) for y in range(self.height)] for x in range(self.width)]
		self.moveState = Board.STATE_MOVE_UNSUCCESSFUL
		self.moveCoordinate = False
		self.moveDirection = Board.DIRECTION_NONE

	def cells(self):
		return self.cells

	def getCellByName(self, i):
		return self.cells[i%self.width][int(i/self.height)]

	def getCellCoordinatesByName(self, i):
		return i%self.width, int(i/self.height)

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
			piece = player.getPiece(action[1])
			if (piece is None):
				return False

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

	def getCoordinatesOfDirection(self, startX, startY, direction, length=1, verbose=True):
		if (not self.isIndexInBounds(startX, startY)):
			if verbose: print("Starting coordinates are out of bounds")
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
			if verbose: print("Unknown direction for coordinates:",direction)
			endX, endY = -1, -1

		if (not self.isIndexInBounds(endX, endY)):
			if verbose: print("Ending coordinates are out of bounds")
			return -1, -1
		else:
			return endX, endY

	def checkFullBoardWin(self):
		#Count who owns more cells on the board (ignoring walls)
		colorCount = {"w":0, "b":0}
		for y in range(self.height):
			for x in range (self.width):
				cell = self.cells[x][y]
				if (cell.owner and cell.road):
					colorCount[cell.owner] += 1
				elif (cell.owner is None):
					return False
		#If they are even, return true
		if (colorCount['w'] == colorCount['b']):
			return True
		else:
			return max(colorCount, key=colorCount.get)

	def checkRoadWin(self, player):
		neighbors = self.getNeighborsList(player)
		return self.checkWinDirection(neighbors, Board.NODE_UP, Board.NODE_DOWN) or \
			   self.checkWinDirection(neighbors, Board.NODE_LEFT, Board.NODE_RIGHT)

	def checkWinDirection(self, neighbors, start, end):
		if (not(
			(start == Board.NODE_UP and end == Board.NODE_DOWN) or
			(start == Board.NODE_DOWN and end == Board.NODE_UP) or
			(start == Board.NODE_LEFT and end == Board.NODE_RIGHT) or
			(start == Board.NODE_RIGHT and end == Board.NODE_LEFT)
			)):
			print("Start/End node missing or not checking win in an acceptable direction")
			return False

		ignoredNodes = []
		if (start == Board.NODE_UP or start == Board.NODE_DOWN):
			ignoredNodes = [Board.NODE_LEFT, Board.NODE_RIGHT]
		else:
			ignoredNodes = [Board.NODE_UP, Board.NODE_DOWN]

		neighborsToVisit = [start]
		visitedNeighbors = []
		while (True):
			#If theres no place left to search, break
			if (len(neighborsToVisit) == 0):
				break

			#Get the next cell to search from the list of non visited cells.
			#Add this cell to the list of visited cells
			currentCell = neighborsToVisit.pop()
			visitedNeighbors.append(currentCell)

			#If you find the 'end' node, return True
			if (currentCell == end):
				print('Found a path from %s to %s! We have a winner!' % (start, end))
				return True

			#If you haven't found the end, keep searching
			#Add the list of the current cell's valid neighbors to the list of cells to visit
			for i in neighbors[currentCell]:
				if (i not in visitedNeighbors and i not in neighborsToVisit and i not in ignoredNodes):
					neighborsToVisit.append(i)
		return False

	def checkTak(self, player):
		neighbors = self.getNeighborsList(player, True)
		return self.checkTakDirection(neighbors, player, Board.NODE_UP, Board.NODE_DOWN) or \
			   self.checkTakDirection(neighbors, player, Board.NODE_LEFT, Board.NODE_RIGHT)

	def checkTakDirection(self, neighbors, player, start, end):
		if (not(
			(start == Board.NODE_UP and end == Board.NODE_DOWN) or
			(start == Board.NODE_DOWN and end == Board.NODE_UP) or
			(start == Board.NODE_LEFT and end == Board.NODE_RIGHT) or
			(start == Board.NODE_RIGHT and end == Board.NODE_LEFT)
			)):
			print("Start/End node missing or not checking Tak in an acceptable direction")
			return False
		startFriendlyNeighbors,startUnfriendlyNeighbors = self.getNodeNeighbors(neighbors, start, player)
		endFriendlyNeighbors,endUnfriendlyNeighbors = self.getNodeNeighbors(neighbors, end, player)
		intersection = set(startUnfriendlyNeighbors) & set(endUnfriendlyNeighbors)

		for i in intersection:
			# If there is an empty cell, return true
			cell = self.getCellByName(i)
			if (cell.placeable):
				return True
			# # If the player has a wall in the way of a road, player may be able to move it and win
			if (cell.owner == player.color[0] and not cell.road and len(cell.pieces) > 2):
				print ("Player may have tak if they move the wall in cell", cell.name)
				return False
			# If there is a wall of either color in the way, player may be able to flatten it and win
			if (cell.flattenable):
				print ("Player may have tak if they can flatten piece in cell", cell.name)
				return False
			# If there is an opposing piece in the way, player may be able to take over it by sliding a stack and win
			if (cell.owner != player.color[0] and cell.stackable):
				print ("Player may have tak if they can slide a stack to take over cell", cell.name)
				print("Searching for towers:", self.searchForTowers(i, player))
				return False
			else:
				return False

	def searchForTowers(self, cellName, player):
		x, y = self.getCellCoordinatesByName(cellName)

		towersByDirection = [[],[],[],[]]
		for direction in range(0, len(Board.LIST_OF_DIRECTIONS)):
			# If we are searching up or down, use height. Else use width
			dimension = self.height-1 if direction < 2 else self.width-1
			for i in range (1, dimension):
				# Get the coordinates of cells in specified direction. If out of bounds, break.
				targetCoordinates = self.getCoordinatesOfDirection(x, y, Board.LIST_OF_DIRECTIONS[direction], i, verbose=False)
				if (targetCoordinates == (-1, -1)):
					break

				# If the tower is tall enough and the player owns the tower, add it to the list
				targetCell = self.cells[targetCoordinates[0]][targetCoordinates[1]]
				if (len(targetCell.pieces) > i and targetCell.owner == player.color[0]):
					towersByDirection[direction].append(targetCoordinates)

		return towersByDirection

	def getPossibleMoves(self, x, y, player, direction=DIRECTION_NONE):
		return False

	def getNodeNeighbors(self, neighbors, node, player):
		ignoredNodes = [Board.NODE_UP, Board.NODE_DOWN, Board.NODE_LEFT, Board.NODE_RIGHT]
		neighborsToVisit = [node]
		visitedNeighbors = []
		unfriendlyNeighbors = []
		while (True):
			#If theres no place left to search, break
			if (len(neighborsToVisit) == 0):
				break

			#Get the next cell to search from the list of non visited cells.
			#Add this cell to the list of visited cells
			currentCell = neighborsToVisit.pop()
			visitedNeighbors.append(currentCell)

			#If you still have places to visit, keep going
			#Add the list of the current cell's friendly neighbors to the list of cells to visit
			for i in neighbors[currentCell]:
				if (i not in visitedNeighbors and i not in neighborsToVisit and i not in unfriendlyNeighbors and i not in ignoredNodes):
					cell = self.getCellByName(i)
					if (cell.owner == player.color[0] and cell.road):
						neighborsToVisit.append(i)
					else:
						unfriendlyNeighbors.append(i)
		visitedNeighbors.remove(node)
		return visitedNeighbors, unfriendlyNeighbors

	def getNeighborsList(self, player, tak=False):
		# Create a dictionary of all the cells.
		# The key will be the cell's name and the value with be the cell's neighbors
		# Add a Up, Down, Left, and Right node to the respective sides of the board
		# The elements will be indexed as such:
		#            up
		#      x 0  1  2  3  4
		#    y _______________
		# l  0 | 0  1  2  3  4  r
		# e  1 | 5  6  7  8  9  i
		# f  2 |10 11 12 13 14  g
		# t  3 |15 16 17 18 19  t
		#    4 |20 21 22 23 24  t
		#           down
		# So self.cells[2][1].name will be cell 7
		neighbors = {}
		for y in range(self.height):
			for x in range (self.width):
				neighbors[y * self.height + x] = []

		neighbors[Board.NODE_UP] = self.getCellNeighbors(None, None, player, tak, Board.NODE_UP)
		neighbors[Board.NODE_DOWN] = self.getCellNeighbors(None, None, player, tak, Board.NODE_DOWN)
		neighbors[Board.NODE_LEFT] = self.getCellNeighbors(None, None, player, tak, Board.NODE_LEFT)
		neighbors[Board.NODE_RIGHT] = self.getCellNeighbors(None, None, player, tak, Board.NODE_RIGHT)

		#Loop through all the board's cells
		for y in range(self.height):
			for x in range(self.width):
				i = y * self.height + x
				# Only add cells that belong to the player to the neighbor's list
				if (self.cells[x][y].owner == player.color[0]):
					#If checking for Tak, find all neighbors for the cell
					#Otherwise, find all friendly neighbors for the cell
					neighbors[i] = self.getCellNeighbors(x, y, player, tak)
		return neighbors

	def getCellNeighbors(self, x, y, player=None, takCheck=False, node=False, length=1):
		# add in the ability to get neighbors for nodes. Also convert nodes to cells
		#initialize the return array
		neighbors = []

		# Coordinate modifiers for directions: Up, Down, Left, Right
		directions = [[0, -1*length, Board.NODE_UP],
						[0, length, Board.NODE_DOWN],
						[-1*length, 0, Board.NODE_LEFT],
						[length, 0, Board.NODE_RIGHT]]

		if(node):
			if (node == Board.NODE_UP):
				for i in range(self.width):
					neighbors.append(self.cells[i][0].name)
			if (node == Board.NODE_DOWN):
				for i in range(self.width):
					neighbors.append(self.cells[i][self.height-1].name)
			if (node == Board.NODE_LEFT):
				for i in range(self.height):
					neighbors.append(self.cells[0][i].name)
			elif (node == Board.NODE_RIGHT):
				for i in range(self.height):
					neighbors.append(self.cells[self.width-1][i].name)
		#If player is passed in, only return friendly neighbors
		elif (player and not takCheck):
			playerColor = player.color[0]
			for i in range(len(directions)):
				calcX, calcY = x+directions[i][0], y+directions[i][1]
				if (self.isIndexInBounds(calcX, calcY) and self.cells[calcX][calcY].owner == playerColor and self.cells[x][y].road):
					neighbors.append(self.cells[calcX][calcY].name)
		#If no player is passed in or we are checking for Tak, return all neighbors
		else:
			for i in range(len(directions)):
				if (self.isIndexInBounds(x+directions[i][0], y+directions[i][1])):
					neighbors.append(self.cells[x+directions[i][0]][y+directions[i][1]].name)
				else:
					neighbors.append(directions[i][2])
		return neighbors

	def __str__(self):
		boardString = ""
		for y in range(self.height):
			for x in range(self.width):
				boardString = boardString + " " + str(self.cells[x][y])
			boardString = boardString + "\n\n"
		return boardString;