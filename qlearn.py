import snake as game
import argparse
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Convolution2D
from keras.optimizers import Adam
import numpy as np
import skimage as skimage
import random
import json
from random import sample as rsample
import time

INPUT_SHAPE = (80, 80, 2)  # Shape of the image imported into the NN
NB_ACTIONS = 5  # NB_ACTIONS is the number of actions the player can do
BATCH = 100
GAME_INPUT = [0, 1, 2, 3, 4]
EPSILON = 1
EPSILON_DECAY = 0.99
FINAL_EPSILON = 0.3
LEARNING_RATE = 1e-4
GAMMA = 0.7
NB_FRAMES = 1