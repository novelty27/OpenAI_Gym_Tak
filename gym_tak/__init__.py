from gym.envs.registration import register

register(
	id='tak-v0',
	entry_point='gym_tak.envs:TakEnv',
)