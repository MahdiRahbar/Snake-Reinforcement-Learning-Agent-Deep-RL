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



def build_model():
    model = Sequential()

    model.add(Convolution2D(16, (8, 8), strides=(4, 4), input_shape=INPUT_SHAPE))
    model.add(Activation("relu"))
    model.add(Convolution2D(32, (4, 4), strides=(2, 2)))  # This layer added instead of the two below layers
    model.add(Activation("relu"))
    # model.add(Convolution2D(32, (4, 4), strides=(4, 4)))
    # model.add(Activation("relu"))
    # model.add(Convolution2D(64, (4, 4), strides=(2, 2)))
    # model.add(Activation("relu"))

    model.add(Flatten())

    # Multi-layer perceptron
    model.add(Dense(1024))
    model.add(Activation("relu"))
    model.add(Dense(512))
    model.add(Activation("relu"))
    model.add(Dense(256))
    model.add(Activation("relu"))
    model.add(Dense(128))
    model.add(Activation("relu"))
    model.add(Dense(64))
    model.add(Activation("relu"))
    
    model.add(Dense(NB_ACTIONS))

    # Compling the model
    adam = Adam(lr=LEARNING_RATE)
    model.compile(loss="mean_squared_error", optimizer=adam)
    print(model.summary())
    return model


