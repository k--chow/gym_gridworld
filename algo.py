import gym
import numpy as np
import numpy, time
import gym_gridworld
import time
import math
import copy
'''
Input: A gridworld with initial grid, reward grid, problem/termination states (fake states), a discount lambda, and the number of iterations
'''
def value_iteration(v, reward_grid, fake_states, discount, iterations):
	'''
	Start from arbitrary end point, or all points
	'''
	# first iteration
	rows = np.shape(reward_grid)[0]
	columns = np.shape(reward_grid)[1]
	for i in range(iterations-1):
		old_v = copy.deepcopy(v)
		print("Discount", (math.pow(discount, i)))
		for x in range(rows):
			for y in range(columns):
				# Check if its a 'fake state'state = (x, y)
				# try all combinations up down left right, protect boundaries
				if (x, y) not in fake_states:
					'''
					up = 0.8*((grid_protection(reward_grid, x, y, x, y+1) + grid_protection(old_v, x, y, x, y+1)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x+1, y) + grid_protection(old_v, x, y, x+1, y)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x-1, y) + grid_protection(old_v, x, y, x-1, y)*(math.pow(discount, i))))
					
					down = 0.8*((grid_protection(reward_grid, x, y, x, y-1) + grid_protection(old_v, x, y, x, y-1)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x+1, y) + grid_protection(old_v, x, y, x+1, y)*(math.pow(discount, i)))) 
					+ 0.1*((grid_protection(reward_grid, x, y, x-1, y) + grid_protection(old_v, x, y, x-1, y)*(math.pow(discount, i))))
					
					left = 0.8*((grid_protection(reward_grid, x, y, x-1, y) + grid_protection(old_v, x, y, x-1, y)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x, y+1) + grid_protection(old_v, x, y, x, y+1)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x, y-1) + grid_protection(old_v, x, y, x, y-1)*(math.pow(discount, i))))
					
					right = 0.8*((grid_protection(reward_grid, x, y, x+1, y) + grid_protection(old_v, x, y, x+1, y)*(math.pow(discount, i)))) 
					+ 0.1*((grid_protection(reward_grid, x, y, x, y+1) + grid_protection(old_v, x, y, x, y+1)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x, y-1) + grid_protection(old_v, x, y, x, y-1)*(math.pow(discount, i))))
					'''
					up = 0.8*((grid_protection(reward_grid, x, y, x, y+1) + grid_protection(old_v, x, y, x, y+1)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x+1, y) + grid_protection(old_v, x, y, x+1, y)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x-1, y) + grid_protection(old_v, x, y, x-1, y)*(math.pow(discount, i))))
					
					down = 0.8*((grid_protection(reward_grid, x, y, x, y-1) + grid_protection(old_v, x, y, x, y-1)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x+1, y) + grid_protection(old_v, x, y, x+1, y)*(math.pow(discount, i)))) 
					+ 0.1*((grid_protection(reward_grid, x, y, x-1, y) + grid_protection(old_v, x, y, x-1, y)*(math.pow(discount, i))))
					
					left = 0.8*((grid_protection(reward_grid, x, y, x-1, y) + grid_protection(old_v, x, y, x-1, y)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x, y+1) + grid_protection(old_v, x, y, x, y+1)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x, y-1) + grid_protection(old_v, x, y, x, y-1)*(math.pow(discount, i))))
					
					right = 0.8*((grid_protection(reward_grid, x, y, x+1, y) + grid_protection(old_v, x, y, x+1, y)*(math.pow(discount, i)))) 
					+ 0.1*((grid_protection(reward_grid, x, y, x, y+1) + grid_protection(old_v, x, y, x, y+1)*(math.pow(discount, i))))
					+ 0.1*((grid_protection(reward_grid, x, y, x, y-1) + grid_protection(old_v, x, y, x, y-1)*(math.pow(discount, i))))
					
					v[x][y] = max([up, down, left, right])
				print(v[x][y], " ", end="")
			print()
		print()
	return 0
'''
If goes out of bounds, stay where you are and return that grid value.
Current x and y are valid.
'''
def grid_protection(gride, current_x, current_y, new_x, new_y):
	rows = np.shape(gride)[0]
	columns = np.shape(gride)[1]
	if (new_x < 0 or new_x >= rows) or (new_y < 0 or new_y >= columns):
		return gride[current_x][current_y]
	return gride[new_x][new_y]

grid = [
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0]
		]

reward_grid = [
				[0, 0, 0, 1],
				[0, 0, 0, -1],
				[0, 0, 0, 0]
				]

fake_states = [(0, 3), (1, 3), (1, 1)]

value_iteration(grid, reward_grid, fake_states, 0.9, 10)


'''
np.random.seed(int(time.time()))
env = gym.make('gridworld-v0')

for i_episode in range(10):
	state = env.reset()
	print(state)
	total_reward = 0
	while 1:
		env.render()
		time.sleep(1)
		action = env.action_space.sample()
		state, reward, done, action_executed = env.step(action)
		print(state, reward, done, action, action_executed)
		total_reward += reward
		if done == 1:
			print("Total Reward", total_reward)
			break
'''

