from .Cell import Cell

class Board: 
	def __init__(self, gameData):
		self.height = gameData[0]
		self.width = gameData[1]
		self.pieces = gameData[2]
		self.capstones = gameData[3]
		self.maxHeight = 2 * (self.pieces + self.capstones)
		self.cells = [[Cell() for x in range(self.width)] for y in range(self.height)]

	def cells(self):
		return self.cells

	def play(self, player, action):
		if (action[0] == "place"):
			piece = action[1][0]
			color = player.color[0]
			x = action[2]
			y = action[3]
			return self.cells[x][y].place(color, piece)
		elif (action[0] == "move"):
			## Stil to be implemented. At first I'm only implementing placing pieces
			startX = action[1]
			startY = action[2]
			stackHeight = action[3]
			endX = action[4]
			endY = action[5]
		else:
			print("Please make a valid move")
			return false

		return true

	def __str__(self):
		boardString = ""
		for x in range(self.width):
			for y in range(self.width):
				boardString = boardString + " " + str(self.cells[x][y])
			boardString = boardString + "\n\n"
		return boardString;