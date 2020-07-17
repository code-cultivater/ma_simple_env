#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simulate a predator prey environment.
Each agent can just observe itself (it's own identity) i.e. s_j = j and vision sqaure around it.
Design Decisions:
    - Memory cheaper than time (compute)
    - Using Vocab for class of box:
         -1 out of bound,
         indexing for predator agent (from 2?)
         ??? for prey agent (1 for fixed case, for now)
    - Action Space & Observation Space are according to an agent
    - Rewards -0.05 at each time step till the time
    - Episode never ends
    - Obs. State: Vocab of 1-hot < predator, preys & units >
"""

# core modules
import random
import math
import curses

# 3rd party modules
import gym
import numpy as np
from gym import spaces


class MeetEnv(gym.Env):
    # metadata = {'render.modes': ['human']}

    def __init__(self,):
        self.__version__ = "0.0.1"

        # TODO: better config handling
        self.episode_over = False

    def init_curses(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_YELLOW, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)
        curses.init_pair(4, curses.COLOR_GREEN, -1)

    def init_args(self, parser):
        env = parser.add_argument_group('Prey Predator task')
        self.dim=5
        self.vision=2
        self.reward=10

    def multi_agent_init(self, args):
        self.n_player = 2
        self.dims= (self.dim, self.dim)
        self.naction = 5
        return

    def reset(self):
        self.episode_over = False
        self.grid=self._set_grid()
        self.players_pos=[[0,0],[self.dim-1,self.dim-1]]
        for i in range(self.n_player):
            player_i_x,player_i_y=self.players_pos[i][0],self.players_pos[i][1]
            self.grid[player_i_x][player_i_y] = self.grid[player_i_x][player_i_y]  + str(i)
        return self._get_obs()

    def _get_obs(self):
        return  [self.players_pos[i] for i in range(self.n_player)].insert(0, self.grid)

    def step(self, action):
        if self.episode_over:
            raise RuntimeError("Episode is done")
        for i, a in enumerate(action):
            self._take_action(i, a)
        assert np.all(action <= self.naction), "Actions should be in the range [0,naction)."
        self.obs = self._get_obs()
        self.episode_over = False
        if(self._get_reward()==self.reward) :self.episode_over=True
        debug = {'player_pos':self.players_pos,'grid':self.grid}
        return self.obs, self._get_reward(), self.episode_over, debug

    def _set_grid(self):
        self.grid=np.full(self.dims,"",dtype=np.object)

    def _take_action(self, idx, act):

        player_i_x,player_i_y=self.players_pos[idx]
        if act==0:
            pass
        # UP
        if act==1 and player_i_x!=0:
            self.grid[player_i_x - 1][player_i_y] =self.grid[player_i_x - 1][player_i_y]+ str(idx)
            self.grid[player_i_x ][player_i_y] = self.grid[player_i_x ][player_i_y].replace(str(idx),"")
            self.players_pos[idx]= [player_i_x - 1,player_i_y]
        # RIGHT
        elif act == 2 and player_i_y != self.dims[1]-1:
            self.grid[player_i_x][player_i_y+1] = self.grid[player_i_x ][player_i_y+1] + str(idx)
            self.grid[player_i_x][player_i_y] = self.grid[player_i_x][player_i_y].replace(str(idx), "")
            self.players_pos[idx] = [player_i_x, player_i_y+1]
        # DOWN
        elif act == 3 and player_i_x != self.dims[0] - 1:
            self.grid[player_i_x+1][player_i_y ] = self.grid[player_i_x+1][player_i_y ] + str(idx)
            self.grid[player_i_x][player_i_y] = self.grid[player_i_x][player_i_y].replace(str(idx), "")
            self.players_pos[idx] = [player_i_x+1, player_i_y]
        # LEFT
        elif act==4 and player_i_y != 0:
            self.grid[player_i_x][player_i_y-1 ] = self.grid[player_i_x][player_i_y-1 ] + str(idx)
            self.grid[player_i_x][player_i_y] = self.grid[player_i_x][player_i_y].replace(str(idx), "")
            self.players_pos[idx] = [player_i_x , player_i_y-1]


    def _get_reward(self):
        if((self.players_pos[0]==self.players_pos[1]).all()):
            return self.reward


