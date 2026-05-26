import random
from collections import deque
from torch.optim.lr_scheduler import StepLR

import torch.optim as optim
from GobbletQNetwork import *

class GobbletDQNAgent:
    def __init__(self, lr=1e-3, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.99):
        self.device = torch.device("cpu" if torch.cuda.is_available() else "cpu")
        self.q_network = GobbletQNetwork().to(self.device)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.memory = deque(maxlen=100000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.target_network = GobbletQNetwork().to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_update_freq = 1000
        self.steps_done = 0
        self.scheduler = StepLR(self.optimizer, step_size=200000, gamma=0.5)

    def save(self, filepath):
        torch.save(self.q_network.state_dict(), filepath)

    def load(self, filepath):
        state_dict = torch.load(filepath, map_location=self.device, weights_only=True)
        self.q_network.load_state_dict(state_dict)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, valid_actions, training=False):
        if not training and self.epsilon == 0.0:
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            q_values = self.q_network(state_tensor).detach().cpu().numpy()[0]
            masked_q = np.full(27, -np.inf, dtype=np.float32)
            for a in valid_actions:
                masked_q[a] = q_values[a]
            return np.argmax(masked_q)
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
                with torch.no_grad():
                    target = reward + self.gamma * torch.max(self.target_network(next_state_tensor)).item()

            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            target_f = self.q_network(state_tensor).detach().cpu().numpy().copy()
            target_f[0][action] = target
            target_tensor = torch.FloatTensor(target_f).to(self.device)

            self.optimizer.zero_grad()
            output = self.q_network(state_tensor)
            loss = self.criterion(output, target_tensor)
            loss.backward()

            torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), max_norm=1.0)

            self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        self.steps_done += 1
        if self.steps_done % self.target_update_freq == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())

        if self.steps_done % 200000 == 0:
            self.scheduler.step()
            print(f"LR updated: {self.optimizer.param_groups[0]['lr']}")

    def save_checkpoint(self, filepath):
        torch.save({
            'model_state_dict': self.q_network.state_dict(),
            'target_model_state_dict': self.target_network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if hasattr(self, 'scheduler') else None,
            'epsilon': self.epsilon,
            'steps_done': self.steps_done,
            'memory': list(self.memory),  # Сериализуем deque в list
            'gamma': self.gamma,
            'epsilon_min': self.epsilon_min,
            'epsilon_decay': self.epsilon_decay,
            'memory_maxlen': self.memory.maxlen,
        }, filepath)
        print(f"Checkpoint saved: {filepath}")

    def load_checkpoint(self, filepath):
        checkpoint = torch.load(filepath, map_location=self.device, weights_only=False)

        self.q_network.load_state_dict(checkpoint['model_state_dict'])
        self.target_network.load_state_dict(checkpoint['target_model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

        if hasattr(self, 'scheduler') and checkpoint.get('scheduler_state_dict'):
            self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

        self.epsilon = checkpoint['epsilon']
        self.steps_done = checkpoint['steps_done']

        self.memory = deque(checkpoint['memory'], maxlen=self.memory.maxlen)

        self.gamma = checkpoint.get('gamma', self.gamma)
        self.epsilon_min = checkpoint.get('epsilon_min', self.epsilon_min)
        self.epsilon_decay = checkpoint.get('epsilon_decay', self.epsilon_decay)

        self.q_network.train()
        self.target_network.train()
        memory_maxlen = checkpoint.get('memory_maxlen', 100_000)  # fallback на дефолт
        self.memory = deque(checkpoint['memory'], maxlen=memory_maxlen)

        print(f"Checkpoint loaded: {filepath} (epsilon={self.epsilon:.4f}, steps={self.steps_done})")
        return checkpoint