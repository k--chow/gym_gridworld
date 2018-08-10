import gym
import numpy as np
import numpy, time
import gym_gridworld
import time
import math
import copy
'''
Input: Reward transition function, value function, and the action taken.
action - [(probability, action)]
Output: Reward for the action taken
'''
def value_iteration_helper(reward_transition, value, discount, state, action):
	reward = 0
	for possible_action in action:
		probability = possible_action[0]
		new_state = possible_action[1]
		transition = (state, new_state)
		reward += probability*(reward_transition.get(transition, 0) + grid_protection(value, state, new_state)*discount)
	return reward


'''
Input: A gridworld with initial grid, reward grid, problem/termination states (fake states), a discount lambda, and the number of iterations
'''
def value_iteration(grid, reward_transition, fake_states, exit_states, policy, discount, iterations=10):
	v = copy.deepcopy(grid)
	rows = np.shape(grid)[0]
	columns = np.shape(grid)[1]
	for i in range(iterations-1):
		old_v = copy.deepcopy(v)
		for x in range(rows):
			for y in range(columns):
				if (x, y) in exit_states:
					# careful 'exit' is not a real state - change value to a dict also
					exit = 1.0*(reward_transition.get( ((x, y), 'exit'), 0) )
					v[x][y] = exit
				elif (x, y) not in fake_states:
					right = value_iteration_helper(reward_transition, old_v, discount, (x, y), [
																									(0.8, (x, y+1)),
																									(0.1, (x+1, y)),
																									(0.1, (x-1, y))
																								])
					left = value_iteration_helper(reward_transition, old_v, discount, (x, y), [
																									(0.8, (x, y-1)),
																									(0.1, (x+1, y)),
																									(0.1, (x-1, y))
																								])
					up = value_iteration_helper(reward_transition, old_v, discount, (x, y), [
																									(0.8, (x-1, y)),
																									(0.1, (x, y+1)),
																									(0.1, (x, y-1))
																								])
					down = value_iteration_helper(reward_transition, old_v, discount, (x, y), [
																									(0.8, (x+1, y)),
																									(0.1, (x, y+1)),
																									(0.1, (x, y-1))
																								])
					v[x][y] = max([up, down, left, right])
					if up == max([up, down, left, right]):
						policy[(x, y)] = 0
					elif down == max([up, down, left, right]):
						policy[(x, y)] = 2
					elif left == max([up, down, left, right]):
						policy[(x, y)] = 3
					else:
						policy[(x, y)] = 1
				#print(v[x][y], " ", end="")
				print(policy.get((x, y), -1), " ", end="")
			print()
		print()
	return 0
'''
If goes out of bounds, stay where you are and return that grid value.
Current x and y are valid.
'''
def grid_protection(gride, state, new_state):
	(current_x, current_y) = state
	(new_x, new_y) = new_state
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

# R(s, a, s')
reward_transition = {
	((0, 3), 'exit'): 1,
	((1, 3), 'exit'): -1,
}

fake_states = [(1, 1)]
exit_states = [(0, 3), (1, 3)]


policy = {}


value_iteration(grid, reward_transition, fake_states, exit_states, policy, 0.9, 10)


np.random.seed(int(time.time()))
env = gym.make('gridworld-v0')
discount = 0.9

for i_episode in range(10):
	state = env.reset()
	print(state)
	total_reward = 0
	state_count = 0
	while 1:
		env.render()
		time.sleep(1)
		action = policy[(state[0], state[1])]
		state, reward, done, action_executed = env.step(action)
		print(state, reward, done, action, action_executed)
		total_reward += reward*(math.pow(discount, state_count))
		state_count += 1 
		if done == 1:
			print("Total Reward", total_reward, "State count", state_count)
			break



