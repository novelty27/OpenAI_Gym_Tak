import gym
from gym import error, spaces, utils
from gym.utils import seeding

class TakEnv(gym.Env):
	metadata = {'render.mods': ['human']}

	def __init__(self):
		print('__init__')

	def step(self, action):
		print('step')

	def reset(self):
		print('reset')

	def render(self, mode='human', close=False):
		print('render')
