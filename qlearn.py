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
FINAL_EPSILON = 0.1
LEARNING_RATE = 1e-4
GAMMA = 0.9
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


def nn_loadOld_weights(model):
    print("Now we load weight")
    model.load_weights("model.h5")
    print("Weight load successfully")
    print("Let the training begin!")
    train_network(model)


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

    while True:

        loss = 0
        Q_sa = 0
        action_index = 4
        r_t = 0
        a_t = "no nothing"
        if terminal:
            game_state.set_start_state()
        if t % NB_FRAMES == 0:
            if random.random() <= epsilon:
                action_index = random.randrange(NB_ACTIONS)
                a_t = GAME_INPUT[action_index]
            else:
                action_index = np.argmax(model.predict(s_t))
                a_t = GAME_INPUT[action_index]
        if epsilon > FINAL_EPSILON:
            epsilon = epsilon * EPSILON_DECAY
        else:
            epsilon = FINAL_EPSILON
        # run the selected action and observed next state and reward
        x_t1_colored, r_t, terminal = game_state.run(a_t)
        s_t1 = stack_image(x_t1_colored)
        experience = (s_t, a_t, r_t, s_t1)
        batch = exp_replay.send(experience)
        s_t1 = stack_image(x_t1_colored)
        if batch:
            inputs = np.zeros((BATCH, s_t.shape[1], s_t.shape[2], s_t.shape[3]))
            targets = np.zeros((BATCH, NB_ACTIONS))
            i = 0
            for s, a, r, s_pred in batch:
                inputs[i : i + 1] = s
                if r < 0:
                    targets[i, a] = r
                else:
                    Q_sa = model.predict(s_pred)
                    targets[i, a] = r + GAMMA * np.max(Q_sa)
                i += 1
            loss += model.train_on_batch(inputs, targets)
            # Exploration vs Exploitation

        t += 1
        # save progress every 10000 iterations
        if t % 100 == 0:
            print("Now we save model")
            model.save_weights("model.h5", overwrite=True)
            with open("model.json", "w") as outfile:
                json.dump(model.to_json(), outfile)

        if t % 10 == 0:
            print(
                "TIMESTEP",
                t,
                "/ EPSILON",
                epsilon,
                "/ ACTION",
                action_index,
                "/ REWARD",
                r_t,
                "/ Q_MAX ",
                np.max(Q_sa),
                "/ Loss ",
                loss,
            )

    print("Episode finished!")
    print("************************")

def nn_playGame(model):
    print("Now we load weight")
    model.load_weights("model.h5")
    print("Weight load successfully")
    print("Let the game begin!")
    game_state = game.Game()  # Starting up a game
    game_state.set_start_state()
    game_image, score, game_lost = game_state.run(
        4
    )  # The game is started but no action is performed
    s_t = stack_image(game_image)
    s_t1 = s_t
    a_t = 4
    while True:

        if game_lost:
            print("Game lost")
            time.sleep(2)
            print("------------------")
            print("Game is restarting")
            game_state.set_start_state()

        action_index = np.argmax(model.predict(s_t1))
        a_t = GAME_INPUT[action_index]
        x_t1_colored, _, terminal = game_state.run(a_t)
        s_t1 = stack_image(x_t1_colored)
        game_lost = terminal


def playGame(args):
    model = build_model()
    if args["mode"] == "Run" or args["mode"] == "run":
        nn_playGame(model)
    elif args["mode"] == "Re-train" or args["mode"] == "re-train" or args["mode"] == "retrain":
        nn_loadOld_weights(model)
    elif args["mode"] == "Train" or args["mode"] == "train":
        train_network(model)
    else:
        print("*** Not valid argument ***")
        print("Run argument for running game with a trained weights")
        print("Re-train argument for continue training model")
        print("Train to train train from scratch")
        print("*********************************")


def main():

    parser = argparse.ArgumentParser(
        description="How you would like your program to run"
    )
    parser.add_argument("-m", "--mode", help="Train / Run / Re-train", required=True)
    args = vars(parser.parse_args())
    playGame(args)



if __name__ == "__main__":
    main()
