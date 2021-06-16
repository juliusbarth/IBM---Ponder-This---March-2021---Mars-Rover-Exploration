# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 00:29:57 2021

@author: jfb2444
"""

import numpy as np
import pandas as pd
from Exploration_IP import solveExplorationPuzzle

# Data
df = pd.read_excel('Data.xlsx',header=None)
rewards = df.to_numpy()
cost = 128
N  = len(rewards)
netRewards = rewards - cost

# Run optimization
cells, objValue, runtime = solveExplorationPuzzle(N, netRewards)   


'''
# Random data
N = 20
cost = 1
reward_mean = 100
reward_var = 1000
rewards = np.random.normal(1,1,(N,N))
rewards = np.around(rewards, 1)
netRewards = np.empty((N, N))  
netRewards = rewards - cost
'''