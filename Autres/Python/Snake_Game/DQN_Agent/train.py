# -*- coding: utf-8 -*-
from dqn_agent import Agent
from DQN import SnakeGame
from dqn_agent import QTrainer


def relative_to_absolute_direction(current_direction, action):
    new_action = None

    # go straight -> garder la meme direction
    if action[1]:
            new_action = current_direction
    elif action[0]:
            new_action = 3 # left
    elif action[2]:
            new_action = 2 # right
            
    return new_action
         


def train():
    agent = Agent()
    game = SnakeGame()
    game.init()

    trainer = QTrainer(agent.model, lr=0.001, gamma=0.9)

    scores = []
    total_score = 0
    high_score = 0
    mean_scores = []


    while True:
        current_state = game.get_state()

        relative_action = agent.get_action(current_state)

        absolute_action = relative_to_absolute_direction(game.snake_head["direction"], relative_action)
       
        reward, done, score = game.step(absolute_action)

        dfghgfdf

        next_state = game.get_state()

        trainer.train_step(current_state, relative_action, reward, next_state, done)

        if done:
              game.init()
              agent.nb_games += 1
              scores.append(score)
              total_score += score 

              if score > high_score:
                    high_score = score
                    agent.model.save()

        print(f"Jeu {agent.n_games}  Score: {score}  Record: {high_score}")


train()