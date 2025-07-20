# -*- coding: utf-8 -*-
from dqn_agent import Agent
from DQN_game_logic import SnakeGame
from dqn_agent import QTrainer
from plot import plot
import pygame

MAX_GAMES = 1000



def train(debug=False):
    agent = Agent()
    agent.load()  # charge le fichier sauvegardé

    game = SnakeGame()
    game.init()

    trainer = QTrainer(agent.model, agent.target_model, agent.optimizer, lr=0.001, gamma=0.9)

    if debug:
        fps = 6.5
        clock = pygame.time.Clock()

    scores = []
    mean_scores = []
    high_score = agent.high_score
    

    try:
        while agent.nb_games < MAX_GAMES:
            current_state = game.get_state()

            relative_action = agent.get_action(current_state)
            absolute_action = game.relative_to_absolute_direction(game.snake_head["direction"], relative_action)

            reward, done, score = game.step(absolute_action)
            next_state = game.get_state()

            agent.memory.push((current_state, relative_action, reward, next_state, done))
            if len(agent.memory) > agent.batch_size:
                minibatch = agent.memory.sample(agent.batch_size)
                states, actions, rewards, next_states, dones = zip(*minibatch)
                trainer.train_step(states, actions, rewards, next_states, dones)

            #trainer.train_step(current_state, relative_action, reward, next_state, done)

            if agent.nb_games % 10 == 0:
                trainer.update_target_model()

            if agent.nb_games % 100 == 0:
                # Sauvegarde régulière
                agent.save()

            if done:
                game.init()
                agent.nb_games += 1

                scores.append(score)
                agent.total_score += score
                mean_score = agent.total_score / agent.nb_games
                mean_scores.append(mean_score)

                plot(scores, mean_scores)

                if score > agent.high_score:
                    high_score = score
                    agent.high_score = high_score
                    print(f"🏆 Nouveau record ! Score: {high_score}")
                
                

            if debug:
                if game.handleDeath() or game.handleFood():
                    game.display_game_over()
                    pygame.time.wait(2000)
                    game.init()
                    continue
                game.updateGame()
                game.drawGrid()
                clock.tick(fps)

            print(f"Jeu {agent.nb_games}  Score: {score}  Record: {agent.high_score}")

    except KeyboardInterrupt:
        print("\n🛑 Entraînement interrompu manuellement.")
        print(f"📊 Nombre de parties jouées : {agent.nb_games}")
        print(f"🏆 Meilleur score atteint : {agent.high_score}")
        print("💾 Sauvegarde du modèle...")

        agent.save()
        plot(scores, mean_scores)
        pygame.quit()

    print("✅ Fin du programme.")

if __name__ == "__main__":
    train(debug=False)
