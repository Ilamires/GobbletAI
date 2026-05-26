import torch
import torch.nn as nn
import torch.nn.functional as F
from Gobblet import *

class GobbletQNetwork(nn.Module):
    def __init__(self, input_size=18, hidden_size=128, output_size=27):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.value_head = nn.Linear(hidden_size, 1)
        self.advantage_head = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        value = self.value_head(x)
        advantage = self.advantage_head(x)
        return value + (advantage - advantage.mean(dim=1, keepdim=True))