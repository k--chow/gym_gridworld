import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random 



class GridWorldEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.action_space = spaces.Discrete(4)
    self.observation_space = spaces.Tuple((spaces.Discrete(4), spaces.Discrete(3)))
    self.states = None
    self.rewards = [[0, 0, 0, 0],[0, 0, 0, -1],[0, 0, 0, 1]]
    self.seed()
    self.max_y = 2
    self.max_x = 3
  # invalid = -1, north = 0, east = 1, south = 2, west = 3
  def check_valid_step(self, action):
    x, y = self.state
    if action == 0 and y == self.max_y:
      return -1 
    if action == 1 and x == self.max_x:
      return -1
    if action == 2 and y == 0:
      return -1
    if action == 3 and x == 0:
      return -1
    return action

  def step(self, action):
    done = 0
    coinflip = random.random()
    x, y = self.state
    new_x, new_y = None, None
    right_angle = 0
    if coinflip < 0.15:
      right_angle = 1
    if coinflip > 0.85:
      right_angle = 2
    # rotate action 90 degrees left or right
    if right_angle == 1:
      action = (action - 1) % 4
    if right_angle == 2:
      action = (action + 1) % 4
    # check if action is legal again
    action = self.check_valid_step(action)
    if action == -1:
      new_x = x
      new_y = y
    elif action == 0:
      new_x = x
      new_y = y+1
    elif action == 1:
      new_x = x +1
      new_y = y
    elif action == 2:
      new_x = x
      new_y = y-1
    else:
      new_x = x-1
      new_y = y
    if (new_x, new_y) == (3, 1) or (new_x, new_y) == (3, 2):
    	done = 1
    self.state = (new_x, new_y)
    reward = self.rewards[self.state[1]][self.state[0]]
    return self.state, reward, done, action

  def reset(self):
    self.state = (3,0)
    return np.array(self.state)

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]
