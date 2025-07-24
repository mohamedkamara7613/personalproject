# -*- coding: utf-8 -*-
"""play_agent.py
This script allows you to play the Snake Game using a trained DQN agent."""
from DQN_game_logic import SnakeGame
from dqn_agent import Agent
import time
import pygame

def play_trained_model():
    agent = Agent()
    agent.load()  # charge le fichier sauvegardé
    game = SnakeGame()
    game.init()

    done = False
    while not done:
        state = game.get_state()
        action = agent.get_action(state)
        direction = game.snake_head["direction"]
        absolute_action = game.relative_to_absolute_direction(direction, action)

        _, done, score = game.step(absolute_action)

        game.drawGrid()
        time.sleep(0.1)  # Pour ralentir un peu

    game.display_game_over()
    pygame.time.wait(2000)
    print(f"Score du modèle : {score}")

if __name__ == "__main__":
    play_trained_model()






# This script allows you to play the Snake Game using a trained DQN agent.
# It initializes the game, loads the trained model, and runs the game loop until the game is over.
# The agent makes decisions based on the current state of the game, and the game is rendered in real-time.
# The final score is printed at the end of the game.
# Make sure to have the trained model saved before running this script.
# You can run this script to see how well the trained agent performs in the Snake Game.
# Ensure that the necessary modules (DQN_game_logic, dqn_agent) are correctly implemented and available in the same directory.
# This script is a simple demonstration of how to use the trained DQN agent to play the game.
# You can modify the game settings or the agent's parameters to see how it affects the performance.
# Enjoy playing with your trained DQN agent in the Snake Game!