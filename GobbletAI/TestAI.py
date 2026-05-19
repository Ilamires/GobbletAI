from time import sleep
from TrainSelfPlay import *
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL1_PATH = os.path.join(SCRIPT_DIR, "gobblet_agent1.pth")
MODEL2_PATH = os.path.join(SCRIPT_DIR, "gobblet_agent2.pth")


def play_vs_random_first(agent, games=100):
    env = Gobblet()
    wins, losses, draws = 0, 0, 0

    for _ in range(games):
        state = env.reset()
        while env.get_valid_actions():
            if env.current_player == 1:
                action = agent.act(state, env.get_valid_actions())
            else:
                action = random.choice(env.get_valid_actions())
            state, reward, done = env.step(action)
            if done or not env.get_valid_actions():
                if reward == 1:
                    wins += 1
                elif reward == -1:
                    losses += 1
                else:
                    draws += 1
                break
    print(f"Результаты за {games} игр: Победы: {wins}, Поражения: {losses}, Ничьи: {draws}")


def play_vs_random_second(agent, games=100):
    env = Gobblet()
    wins, losses, draws = 0, 0, 0

    for _ in range(games):
        state = env.reset()
        while env.get_valid_actions():
            if env.current_player == 1:
                action = random.choice(env.get_valid_actions())
            else:
                action = agent.act(state, env.get_valid_actions())
            state, reward, done = env.step(action)
            if done or not env.get_valid_actions():
                if reward == 1:
                    wins += 1
                elif reward == -1:
                    losses += 1
                else:
                    draws += 1
                break
    print(f"Результаты за {games} игр: Победы: {wins}, Поражения: {losses}, Ничьи: {draws}")


def play_agents(agent1, agent2, games=100):
    env = Gobblet()
    wins1, wins2, draws = 0, 0, 0

    for _ in range(games):
        state = env.reset()
        while env.get_valid_actions():
            valid_actions = env.get_valid_actions()
            if not valid_actions:
                draws += 1
                break

            if env.current_player == 1:
                action = agent1.act(state, valid_actions)
            else:
                action = agent2.act(state, valid_actions)

            state, reward, done = env.step(action)
            if done or not env.get_valid_actions():
                if env.current_player == 1:
                    if reward == 1:
                        wins2 += 1
                    elif reward == -1:
                        wins1 += 1
                    else:
                        draws += 1
                else:
                    if reward == 1:
                        wins1 += 1
                    elif reward == -1:
                        wins2 += 1
                    else:
                        draws += 1
                break

    print(f"Результаты за {games} игр: Агент1 — {wins1}, Агент2 — {wins2}, Ничьи — {draws}")


def check_weight(model_path):
    return os.path.isfile(model_path)


def main():
    for line in sys.stdin:
        command = line.strip()

        if command == "CHECK_WEIGHTS":
            exists = check_weight(MODEL1_PATH) and check_weight(MODEL2_PATH)
            print("true" if exists else "false")
            sys.stdout.flush()
        elif command == "START_TRAINING_IF_NEEDED":
            agent1 = GobbletDQNAgent()
            agent2 = GobbletDQNAgent()
            model1_path = "gobblet_agent1.pth"
            model2_path = "gobblet_agent2.pth"
            try:
                agent1.load(model1_path)
                agent2.load(model2_path)
            except FileNotFoundError:
                agent1, agent2 = train_self_play(episodes=10000)
                agent1.save(model1_path)
                agent2.save(model2_path)
            print("TRAINING_FINISHED")
            sys.stdout.flush()
        elif command == "EXIT":
            break


if __name__ == "__main__":
    main()
    # agent1 = GobbletDQNAgent()
    # agent2 = GobbletDQNAgent()
    # model1_path = "gobblet_agent1.pth"
    # model2_path = "gobblet_agent2.pth"
    # try:
    #     agent1.load(model1_path)
    #     agent2.load(model2_path)
    #     print("Загружена ранее обученная модель!")
    # except FileNotFoundError:
    #     print("Модель не найдена. Начинаем обучение с нуля...")
    #     sleep(1)
    #     agent1, agent2 = train_self_play(episodes=10000)
    #     agent1.save(model1_path)
    #     agent2.save(model2_path)
    #     print("Модель сохранена!")
    #
    # play_agents(agent1, agent2, games=10000)
    # play_vs_random_first(agent1, games=10000)
    # play_vs_random_second(agent2, games=10000)
