# -*- coding: utf-8 -*-
import random
import numpy as np
from collections import deque
import torch
import torch.nn as nn
import torch.optim as optim

MAX_LEN = 100_000

# ------------------------------------------------------------------------------------------------------------------------------
#       .......................................=== Agent ===.......................................
# ------------------------------------------------------------------------------------------------------------------------------


class Agent:
    def __init__(self):
        self.nb_games = 0           # nombre de parties jouées, pour ajuster l'exploration plutard
        self.epsilon = 1.0          # probabilité initiale d'exploration
        self.epsilon_decay = 0.001  # Taux de reduction d'epsilon
        self.epsilon_min = 0.1
        self.gamma = 0.9            # Discount factor


        self.memory = deque(maxlen=MAX_LEN)
        self.batch_size = 1000

        #self.model = Linear_QNet(11, 256, 3)    # input=11, hidden=256, output=3 (left, straight, right)
        #self.trainer = QTrainer(self.model, lr=0.001 , self.gamma)

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



# ------------------------------------------------------------------------------------------------------------------------------
#       .......................................=== Trainer ===.......................................
# ------------------------------------------------------------------------------------------------------------------------------

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = torch.optim.Adam(model.parameters(), lr=self.lr)
        self.loss_fn = torch.nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):

        # Conversion des données en vecteur torch
        state = torch.tensor(state, dtype=torch.float32)
        next_state = torch.tensor(next_state, dtype=torch.float32)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float32)
        done = torch.tensor(done, dtype=torch.bool)

        # Ajout d'une dimension batch fictive (1, etat)
        if len(state.shape) == 1:
            state = state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            action = action.unsqueeze(0)
            reward = reward.unsqueeze(0)
            done = done.unsqueeze(0)

        # Prediction des Q-values pour l'etat courant
        prediction = self.model(state)

        # Calcul de la Q-value cible
        target = prediction.clone()
        for i in range(len(done)):
            Q_new = reward[i]
            if not done[i]:
                Q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))

            target[i][action[i]] = Q_new

        # Calcul de la perte + retropropagation
        self.optimizer.zero_grad()
        loss = self.loss_fn(target, prediction)
        loss.backward()
        self.optimizer.step()

        




"""













"""