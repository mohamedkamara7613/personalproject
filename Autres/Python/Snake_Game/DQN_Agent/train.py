# -*- coding: utf-8 -*-
from dqn_agent import Agent
from DQN_game_logic import SnakeGame
from dqn_agent import QTrainer
from plot import plot
import pygame

MAX_GAMES = 1000



def train(debug=False):
    agent = Agent()
    game = SnakeGame()
    game.init()

    if debug:
        fps = 6.5
        clock = pygame.time.Clock()

    trainer = QTrainer(agent.model, lr=0.001, gamma=0.9)

    scores = []
    total_score = 0
    high_score = 0
    mean_scores = []

    try:
        while agent.nb_games < MAX_GAMES:
            current_state = game.get_state()

            relative_action = agent.get_action(current_state)
            absolute_action = game.relative_to_absolute_direction(game.snake_head["direction"], relative_action)

            reward, done, score = game.step(absolute_action)
            next_state = game.get_state()

            trainer.train_step(current_state, relative_action, reward, next_state, done)

            if done:
                game.init()
                agent.nb_games += 1

                scores.append(score)
                total_score += score
                mean_score = total_score / agent.nb_games
                mean_scores.append(mean_score)

                plot(scores, mean_scores)

                if score > high_score:
                    high_score = score
                    agent.model.save()

            if debug:
                if game.handleDeath() or game.handleFood():
                    game.display_game_over()
                    pygame.time.wait(2000)
                    game.init()
                    continue
                game.updateGame()
                game.drawGrid()
                clock.tick(fps)

            print(f"Jeu {agent.nb_games}  Score: {score}  Record: {high_score}")

    except KeyboardInterrupt:
        print("\n🛑 Entraînement interrompu manuellement.")
        print(f"📊 Nombre de parties jouées : {agent.nb_games}")
        print(f"🏆 Meilleur score atteint : {high_score}")
        print("💾 Sauvegarde du modèle...")

        agent.model.save()
        plot(scores, mean_scores)
        pygame.quit()

    print("✅ Fin du programme.")

if __name__ == "__main__":
    train(debug=False)
