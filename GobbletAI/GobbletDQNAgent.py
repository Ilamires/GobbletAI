import random
from collections import deque

import torch.optim as optim
from GobbletQNetwork import *

class GobbletDQNAgent:
    def __init__(self, lr=1e-3, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.q_network = GobbletQNetwork().to(self.device)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.memory = deque(maxlen=2000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

    def save(self, filepath):
        torch.save(self.q_network.state_dict(), filepath)

    def load(self, filepath):
        state_dict = torch.load(filepath, map_location=self.device, weights_only=True)
        self.q_network.load_state_dict(state_dict)
        self.q_network.eval()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, valid_actions):
        if np.random.rand() <= self.epsilon:
            return random.choice(valid_actions)

        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        q_values = self.q_network(state_tensor).detach().cpu().numpy()[0]

        masked_q = np.full(27, -np.inf, dtype=np.float32)
        for a in valid_actions:
            masked_q[a] = q_values[a]
        return np.argmax(masked_q)

    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            target = reward
            if not done:
                next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0).to(self.device)
                target = reward + self.gamma * torch.max(self.q_network(next_state_tensor)).item()
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            target_f = self.q_network(state_tensor).detach().cpu().numpy()
            target_f[0][action] = target
            target_tensor = torch.FloatTensor(target_f).to(self.device)

            self.optimizer.zero_grad()
            output = self.q_network(state_tensor)
            loss = self.criterion(output, target_tensor)
            loss.backward()
            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay