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


def experience_replay(batch_size):
    memory = []
    while True:
        experience = (
            yield rsample(memory, batch_size) if batch_size <= len(memory) else None
        )
        memory.append(experience)

def stack_image(game_image):
    x_t = skimage.color.rgb2gray(game_image)    # Make image black and white
    x_t = skimage.transform.resize(x_t, (80, 80))    # Resize the image to 80x80 pixels
    x_t = skimage.exposure.rescale_intensity(x_t, out_range=(0, 255))    # Change the intensity of colors, maximizing the intensities.
    s_t = np.stack((x_t, x_t), axis=2)    # Stacking 2 images for the agent to get understanding of speed
    s_t = s_t.reshape(1, s_t.shape[0], s_t.shape[1], s_t.shape[2])    # Reshape to make keras like it
    return s_t

def train_network(model):

    epsilon = EPSILON
    game_state = game.Game()  # Starting up a game
    game_state.set_start_state()
    game_image, score, game_lost = game_state.run(
        0
    )  # The game is started but no action is performed
    s_t = stack_image(game_image)
    terminal = False
    t = 0
    exp_replay = experience_replay(BATCH)
    exp_replay.__next__()  # Start experience replay coroutine