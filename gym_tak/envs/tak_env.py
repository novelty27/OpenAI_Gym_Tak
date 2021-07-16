import gym
from gym import error, spaces, utils
from gym.utils import seeding

from .Board import Board
from .Player import Player 

class TakEnv(gym.Env):
	metadata = {'render.mods': ['human']}
	gameDataByBoardSize = {3:[3, 3, 10, 0], 4:[4, 4, 15, 0], 5:[5, 5, 21, 1], 6:[6, 6, 30, 1], 7:[7, 7, 40, 2], 8:[8, 8, 50, 2]}
	playerNames = ["Albus", "Beaux"]
	playerColors = ["white", "black"]

	def __init__(self, boardSize=5):
		self.board = Board(self.gameDataByBoardSize[boardSize])
		self.player1 = Player(
						self.playerNames[0], 
						self.playerColors[0], 
						self.gameDataByBoardSize[boardSize][2], 
						self.gameDataByBoardSize[boardSize][3])
		self.player2 = Player(
						self.playerNames[1], 
						self.playerColors[1], 
						self.gameDataByBoardSize[boardSize][2], 
						self.gameDataByBoardSize[boardSize][3])
		self.currentPlayer = self.player1

	def step(self, action):
		play = self.board.play(self.currentPlayer, action)
		if (play == Board.STATE_MOVE_SUCCESSFUL):
			self.switchPlayer()
			return play
		elif (play == Board.STATE_MOVE_UNSUCCESSFUL):
			return play
		elif (play == Board.STATE_MOVE_CONTINUE):
			return play
		else:
			print("Unknown state after move:", play)
			return False

	def checkWin(self):
		""" Temporary method to allow end user to test winning functionality """
		hasWon = self.board.checkWin(self.currentPlayer)
		return hasWon

	def reset(self):
		self.board = None
		self.player1 = None
		self.player2 = None
		return self.__init__()

	def render(self, mode='human', close=False):
		output = self.currentPlayer.color + "`s turn\n" + str(self.board) + '\n'
		return output

	def switchPlayer(self):
		if (self.currentPlayer == self.player1):
			self.currentPlayer = self.player2
		else:
			self.currentPlayer = self.player1

	def whichPlayersTurn(self):
		return self.currentPlayer.color