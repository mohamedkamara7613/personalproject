# -*- coding: utf-8 -*-
"""
    Model definition for the DQN agent in Snake Game.

    This module defines the neural network architecture used by the DQN agent.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Linear_QNet, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)

        return x
    
    def save(self, file_name="model.pth"):
        torch.save(self.state_dict(), file_name)

    def load(self, file_name="model.pth"):
        self.load_state_dict(torch.load(file_name))
    