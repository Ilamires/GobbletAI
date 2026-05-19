from GobbletDQNAgent import *
import numpy as np
import tqdm
import sys

def train_self_play(episodes=10000):
    env = Gobblet()
    agent1 = GobbletDQNAgent()
    agent2 = GobbletDQNAgent()

    pbar = tqdm.tqdm(total=episodes, desc="Self-play обучение", unit=" эпизод", colour="cyan")
    scores1, scores2 = [], []

    for e in range(episodes):
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

        agent1.replay()
        agent2.replay()

        avg_r1 = np.mean(scores1[-100:]) if scores1 else 0.0
        avg_r2 = np.mean(scores2[-100:]) if scores2 else 0.0
        pbar.set_postfix({
            "Eps1": f"{agent1.epsilon:.3f}",
            "Eps2": f"{agent2.epsilon:.3f}",
            "AvgR1": f"{avg_r1:.2f}",
            "AvgR2": f"{avg_r2:.2f}"
        })
        pbar.update(1)

        if (e + 1) % 100 == 0 or e == episodes - 1:
            progress = (e + 1) / episodes * 100
            print(f"PROGRESS {progress:.1f}")
            sys.stdout.flush()

        if e % 2000 == 0 and e > 0:
            agent1.save(f"agent1_backup.pth")
            agent2.save(f"agent2_backup.pth")

    pbar.close()

    return agent1, agent2