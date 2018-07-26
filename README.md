## GridWorld Gym Environment
**********

GridWorld is a common MDP (Markov Decision Process) used in teaching AI and Reinforcement Learning. This is an environment you can import and implement basic algorithms on. The states and actions are discrete.

![alt text](https://raw.githubusercontent.com/k--chow/gym_gridworld/master/gridworld.gif "Demo")

```
git clone https://github.com/k--chow/gym_gridworld.git
cd gym_gridworld
pip install -e .
```

To use in code:
```
import gym
import gym_gridworld

env = gym.make('gridworld-v0')
```
### Actions
```
action = 0 # move north
action = 1 # move east
action = 2 # move south
action = 3 # move west
```

### Observation Space
This is a 3 x 4 grid.

###
Gridworld has a rock which is an invalid state, and two exit/game ending states (red and green), which return reward -1 and 1 respectively. MDP's are special because an intentional action is not deterministic; If we choose to go north (action 0), there is a 0.7 probability we go north, and a 0.15 probability we go in each orthogonal direction (0.15 east, 0.15 west).

### Challenge: Algorithms to implement
[] Policy Evaluation
[] TD Learning
[] Monte Carlo
[] Value Iteration
[] Policy Iteration

### TODO
[x] Add visual rendering