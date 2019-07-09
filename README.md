# Snake-Reinforcement-Learning-Agent-Deep-RL

## Description 
As the repo's name indicates, this is a simple Deep-QLearning Agent that learns how to play the famous snake game! However, I believe with some little changes based on other environments it can be adapted to be trained on other games as well. (I have not tested yet!) 
This project was presented as one of the neural network's classes of professor [Dr. Mohammad Manthouri](https://www.linkedin.com/in/mohammad-mansouri-07030766/).

## How to Run?
First make sure to install following packages: Keras, pygame 
```
pip install tensorflow , Keras , pygame 
```
Then you can run the code and train the agent by the following command (Note that it may take several hours for the agent to get to some  acceptable points! So it's all normal!) : 
``` 
python qlearn.py -m "Train"
```
For running the agent with the current saved model you have to enter the following command in the same directory:
``` 
python qlearn.py -m "Run"
```