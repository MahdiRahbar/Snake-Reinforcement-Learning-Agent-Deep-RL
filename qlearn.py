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