# -*- coding: utf-8 -*-
from DQN_game_logic import SnakeGame
from dqn_agent import Agent
import time

def play_trained_model():
    agent = Agent()
    agent.model.load()  # charge le fichier sauvegardé
    game = SnakeGame()
    game.init()

    done = False
    while not done:
        state = game.get_state()
        action = agent.get_action(state)
        direction = game.snake_head["direction"]
        absolute_action = relative_to_absolute_direction(direction, action)

        reward, done, score = game.step(absolute_action)

        game.render()  # Affiche la partie
        time.sleep(0.1)  # Pour ralentir un peu

    print(f"Score du modèle : {score}")
"