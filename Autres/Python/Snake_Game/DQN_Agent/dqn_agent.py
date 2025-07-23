# -*- coding: utf-8 -*-
"""dqn_agent.py
DQN Agent for Snake Game.
This module defines the DQN agent, its memory, and the trainer for training the agent.
"""

import random
import numpy as np
from collections import deque
import torch
import pickle
import os

from model import Linear_QNet

MAX_LEN = 100_000

# ------------------------------------------------------------------------------------------------------------------------------
#       .......................................=== Agent ===.......................................
# ------------------------------------------------------------------------------------------------------------------------------


class Agent:
    def __init__(self):
        self.nb_games = 0           # nombre de parties jouées, pour ajuster l'exploration plutard
        self.high_score = 0         # meilleur score atteint
        self.total_score = 0        # score total pour calculer la moyenne
        self.scores = []            # liste des scores pour le graphique
        self.mean_scores = []       # liste des scores moyens pour le graphique
        self.epsilon = 1.0          # probabilité initiale d'exploration
        self.epsilon_decay = 0.001  # Taux de reduction d'epsilon
        self.epsilon_min = 0.1
        self.gamma = 0.9            # Discount factor
        self.lr = 0.001             # Learning rate

        self.memory = Memory(capacity=MAX_LEN)  # mémoire pour stocker les expériences
        self.batch_size = 1000

        self.model = Linear_QNet(11, 256, 3)    # input=11, hidden=256, output=3 (left, straight, right)
        self.target_model = Linear_QNet(self.model.linear1.in_features,
                                        self.model.linear1.out_features,
                                        self.model.linear2.out_features)
        self.target_model.load_state_dict(self.model.state_dict())  # copie initiale
        self.target_model.eval()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

# ------------------------------------------------------------------------------------------------------------------------------
    def get_action(self, state):
        self.epsilon = max(self.epsilon - self.epsilon_decay, self.epsilon_min)  # diminue epsilon à chaque appel
        final_move = [0, 0, 0] # one-hot encoding


        # A chaque fois l'agent IA a deux choix
        if random.random() < self.epsilon:
            # Exploration : action aleatoire
            action = random.randint(0,2)
        else:
            # Exploitation avec le plus haut Q, il utilise ce qu'il sait deja
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)    # transforme en reseau de neurone
            prediction = self.model(state_tensor)                                   # le model fait un choix
            action = torch.argmax(prediction).item()                                # conversion en entier python

        final_move[action] = 1 # conversion en vecteur binaire

        return final_move
# ------------------------------------------------------------------------------------------------------------------------------
                                                                                                                                                                                                    
    def save(self, file_name="model.pth", memory_path="memory.pkl", score_path="scores.pkl"):
        checkpoint = {
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimizer.state_dict(),
            "nb_games": self.nb_games,
            "high_score": self.high_score,  # optionnel si vous voulez sauvegarder le score
            "total_score": self.total_score
        }
        torch.save(checkpoint, file_name)
        print(f"✅ Modèle sauvegardé dans {file_name}")

        # Sauvegarde du score pour le graphique
        with open(score_path, "wb") as f:
            pickle.dump((self.scores, self.mean_scores), f)

        # Sauvegarde de la mémoire
        with open(memory_path, "wb") as f:
            pickle.dump(self.memory, f)
            print(f"✅ Mémoire sauvegardée dans {memory_path}")
# ------------------------------------------------------------------------------------------------------------------------------

    def load(self, file_name="model.pth", memory_path="memory.pkl", score_path="scores.pkl"):
        if not os.path.exists(file_name) or not os.path.exists(memory_path) or not os.path.exists(score_path):
            print(f"❌ Le fichier {file_name} n'existe pas. Le Fichier va etre créer.")
            self.save(file_name)
            return

        checkpoint = torch.load(file_name)
        self.model.load_state_dict(checkpoint["model_state"])
        self.target_model.load_state_dict(checkpoint["model_state"])  # pour synchroniser
        self.optimizer.load_state_dict(checkpoint["optimizer_state"])
        self.nb_games = checkpoint["nb_games"]
        self.high_score = checkpoint.get("high_score", 0)  # charge le high score s'il existe
        self.total_score = checkpoint.get("total_score", 0)  # charge le score total s'il existe
        self.model.eval()
        self.target_model.eval()  # met le modèle cible en mode évaluation
        
        print(f"📦 Modèle chargé depuis {file_name}, nb_games = {self.nb_games}")

        # Chargement des scores pour le graphique
        if os.path.exists(score_path):
            with open(score_path, "rb") as f:
                self.scores, self.mean_scores = pickle.load(f)
                print("📊 Scores chargés pour le graphique.")

        # Chargement de la mémoire
        if os.path.exists(memory_path):
            with open(memory_path, "rb") as f:
                self.memory = pickle.load(f)
                print(f"📦 Mémoire chargée depuis {memory_path}")




# ------------------------------------------------------------------------------------------------------------------------------
#       .......................................=== Trainer ===.......................................
# ------------------------------------------------------------------------------------------------------------------------------

class QTrainer:
    def __init__(self, model, target_model, optimizer, lr, gamma):
        self.model = model
        self.target_model = target_model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optimizer
        self.loss_fn = torch.nn.MSELoss()

# ------------------------------------------------------------------------------------------------------------------------------

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

# ------------------------------------------------------------------------------------------------------------------------------

    def train_step(self, states, actions, rewards, next_states, dones):

        # Conversion en tenseurs
        states = torch.tensor(np.array(states), dtype=torch.float32)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)     # shape: (batch,)
        rewards = torch.tensor(rewards, dtype=torch.float32)  # shape: (batch,)
        dones = torch.tensor(dones, dtype=torch.bool)         # shape: (batch,)

        # Prédictions actuelles
        predictions = self.model(states)  # shape: (batch, num_actions)
        
        # Clone pour former les cibles
        targets = predictions.clone().detach()

        for i in range(len(dones)):
            Q_new = rewards[i]
            if not dones[i]:
                # Ici on utilise target_model pour stabilité
                Q_new = rewards[i] + self.gamma * torch.max(self.target_model(next_states[i])).item()

            targets[i][actions[i]] = Q_new

        # Calcul de la perte
        self.optimizer.zero_grad()
        loss = self.loss_fn(predictions, targets)
        loss.backward()
        self.optimizer.step()


# ------------------------------------------------------------------------------------------------------------------------------
#       .......................................=== Memory ===.......................................
# ------------------------------------------------------------------------------------------------------------------------------



class Memory:
    def __init__(self, capacity=MAX_LEN):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states),
            np.array(actions),
            np.array(rewards),
            np.array(next_states),
            np.array(dones)
        )

    def __len__(self):
        return len(self.buffer)


