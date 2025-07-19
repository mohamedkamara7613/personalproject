# -*- coding: utf-8 -*-
from dqn_agent import Agent
from DQN import SnakeGame
from dqn_agent import QTrainer
from plot import plot

def relative_to_absolute_direction(current_direction, action):
    directions = ['up', 'right', 'down', 'left']
    idx = directions.index(current_direction)

    if action[1]:  # tout droit
        new_direction = directions[idx]
    elif action[0]:  # à gauche
        new_direction = directions[(idx - 1) % 4]
    elif action[2]:  # à droite
        new_direction = directions[(idx + 1) % 4]

    mapping = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
    return mapping[new_direction]

         


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
        print(done)

        next_state = game.get_state()

        trainer.train_step(current_state, relative_action, reward, next_state, done)

        if done:
            game.init()
            agent.nb_games += 1

            # par rapport a ce bloc
            scores.append(score)
            total_score += score
            mean_score = total_score / agent.nb_games
            mean_scores.append(mean_score)

            plot(scores, mean_scores) 

            if score > high_score:
                high_score = score
                agent.model.save()

        print(f"Jeu {agent.nb_games}  Score: {score}  Record: {high_score}")


train()