import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random 
from gym.envs.classic_control import rendering

class GridWorldEnv(gym.Env):
  metadata = {
    'render.modes': ['human', 'rgb_array'],
    'video.frames_per_second': 50
  }

  def __init__(self):
    self.action_space = spaces.Discrete(4)
    self.observation_space = spaces.Tuple((spaces.Discrete(4), spaces.Discrete(3)))
    self.states = None
    self.rewards = [[0, 0, 0, 0],[0, 0, 0, -1],[0, 0, 0, 1]]
    self.seed()
    self.max_y = 2
    self.max_x = 3
    self.viewer = None
    self.rock = (1, 1)
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
    
    # check if rock
    if (new_x, new_y) == self.rock:
        new_x = x
        new_y = y

    if (new_x, new_y) == (3, 1) or (new_x, new_y) == (3, 2):
    	done = 1
    self.state = (new_x, new_y)
    reward = self.rewards[self.state[1]][self.state[0]]
    return self.state, reward, done, action

  def reset(self):
    self.state = (3,0)
    return np.array(self.state)

  def render(self, mode='human'):
    x, y = self.state
    screen_width = 400
    screen_height = 300
    robot_height = 20
    robot_width = 10
    offset = 50
    grid_center_x = (x+1)*100 - offset
    grid_center_y = (y+1)*100 - offset
    if self.viewer is None:
        self.viewer = rendering.Viewer(screen_width, screen_height)
        rock = rendering.FilledPolygon([(1*100, 1*100), (1*100, 2*100), (2*100, 2*100), (2*100, 1*100)])
        rock.set_color(.8,.6,.4)
        green = rendering.FilledPolygon([(3*100, 1*100), (3*100, 2*100), (4*100, 2*100), (4*100, 1*100)])
        green.set_color(0,1,0)
        red = rendering.FilledPolygon([(3*100, 2*100), (3*100, 3*100), (4*100, 3*100), (4*100, 2*100)])
        red.set_color(1,0,0)
        self.viewer.add_geom(rock)
        self.viewer.add_geom(green)
        self.viewer.add_geom(red)
    l,r,t,b = grid_center_x - robot_width/2, grid_center_x + robot_width/2, grid_center_y + robot_height/2, grid_center_y - robot_height/2
    robot = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
    #self.robottrans = rendering.Transform()
    #robot.add_attr(self.robottrans)
    self.viewer.add_onetime(robot)

    if self.state is None:
        return None
    self.viewer.draw_line((0, 100), (screen_width, 100))
    self.viewer.draw_line((0, 200), (screen_width, 200))
    self.viewer.draw_line((100, 0), (100, screen_height))
    self.viewer.draw_line((200, 0), (200, screen_height))
    self.viewer.draw_line((300, 0), (300, screen_height))
    #self.robottrans.set_translation(-100, 100)


    return self.viewer.render(return_rgb_array = mode=='rgb_array')

  def close(self):
    if self.viewer: self.viewer.close()

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]

