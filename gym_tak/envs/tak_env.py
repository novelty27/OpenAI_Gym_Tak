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

	def step(self, action):
		return self.board.play(self.player1, action)

	def reset(self):
		self.board = None
		self.player1 = None
		self.player2 = None
		return self.__init__()

	def render(self, mode='human', close=False):
		output = str(self.board) + '\n' + self.player1.name + "\n" + self.player2.name
		return output
