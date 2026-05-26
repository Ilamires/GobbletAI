import random
from Gobblet import Gobblet
from GobbletDQNAgent import *
import numpy as np
import tqdm
import sys
import os
from collections import deque
import torch


def evaluate_vs_random(agent, games=100):
    wins = 0
    for _ in range(games):
        test_env = Gobblet()
        state = test_env.reset()
        done = False

        while not done:
            valid_actions = test_env.get_valid_actions()
            if not valid_actions:
                break

            if test_env.current_player == 1:
                saved_eps = agent.epsilon
                agent.epsilon = 0.0
                action = agent.act(state, valid_actions)
                agent.epsilon = saved_eps
            else:
                action = random.choice(valid_actions)

            state, reward, done = test_env.step(action)

            if done:
                if reward == 1:
                    wins += 1
                break
    return wins

def train_self_play(episodes=1000000, checkpoint_path=None, start_episode=0):
    env = Gobblet()
    agent1 = GobbletDQNAgent(
        lr=3e-4,
        gamma=0.99,
        epsilon=1.0,
        epsilon_min=0.001,
        epsilon_decay=0.99999
    )
    agent2 = GobbletDQNAgent(
        lr=3e-4,
        gamma=0.99,
        epsilon=1.0,
        epsilon_min=0.001,
        epsilon_decay=0.99999  # ~100k эпизодов до минимума
    )

    if checkpoint_path and os.path.exists(checkpoint_path):
        print(f"Resuming from checkpoint: {checkpoint_path}")
        agent1.load_checkpoint(checkpoint_path)
        agent2.load_checkpoint(checkpoint_path.replace('agent1', 'agent2'))
    elif start_episode > 0:
        print(f"Warning: start_episode={start_episode}, но чекпоинт не найден")

    pbar = tqdm.tqdm(total=episodes, initial=start_episode, desc="Self-play обучение", unit=" эпизод", colour="cyan")
    scores1, scores2 = [], []

    for e in range(start_episode, episodes):
        state = env.reset()
        done = False
        total_reward1 = 0
        total_reward2 = 0

        while not done:
            valid_actions = env.get_valid_actions()
            if not valid_actions:
                total_reward1 += 0.5
                total_reward2 += 0.5
                done = True
            else:
                if env.current_player == 1:
                    action = agent1.act(state, valid_actions)
                    next_state, reward, done = env.step(action)
                    total_reward1 += reward
                    total_reward2 -= reward
                    agent1.remember(state, action, reward, next_state, done)
                else:
                    action = agent2.act(state, valid_actions)
                    next_state, reward, done = env.step(action)
                    total_reward2 += reward
                    total_reward1 -= reward
                    agent2.remember(state, action, reward, next_state, done)
                state = next_state

        scores1.append(total_reward1)
        scores2.append(total_reward2)

        agent1.replay(batch_size=64)
        agent2.replay(batch_size=64)

        avg_r1 = np.mean(scores1[-100:]) if scores1 else 0.0
        avg_r2 = np.mean(scores2[-100:]) if scores2 else 0.0
        pbar.set_postfix({
            "Eps1": f"{agent1.epsilon}",
            "Eps2": f"{agent2.epsilon}",
            "AvgR1": f"{avg_r1}",
            "AvgR2": f"{avg_r2}"
        })
        pbar.update(1)

        if (e + 1) % 50000 == 0:
            print(f"\n=== EVALUATION at episode {e + 1} ===")
            agent1.q_network.eval()

            wins = evaluate_vs_random(agent1, games=100)
            print(f"Win rate vs random: {wins / 100:.2%}")

            agent1.q_network.train()

        if (e + 1) % 5000 == 0:
            agent1.save_checkpoint(f"checkpoints/agent1_ep{e + 1}.pt")  # .pt для полного чекпоинта
            agent2.save_checkpoint(f"checkpoints/agent2_ep{e + 1}.pt")

            with open("training_log.txt", "a") as f:
                f.write(f"{e + 1},{agent1.epsilon},{avg_r1:.3f}\n")

        if (e + 1) % 100 == 0 or e == episodes - 1:
            progress = (e + 1) / episodes * 100
            print(f"PROGRESS {progress:.1f}")
            sys.stdout.flush()

        if e % 2000 == 0 and e > 0:
            agent1.save(f"agent1_backup.pth")
            agent2.save(f"agent2_backup.pth")

    pbar.close()

    agent1.save_checkpoint("checkpoints/agent1_final.pt")
    agent2.save_checkpoint("checkpoints/agent2_final.pt")

    return agent1, agent2