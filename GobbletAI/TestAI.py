from asyncio.windows_events import NULL
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
    env = None
    agents = [GobbletDQNAgent(), GobbletDQNAgent()]
    global agent1
    global agent2
    model1_path = "gobblet_agent1.pth"
    model2_path = "gobblet_agent2.pth"
    agent1 = GobbletDQNAgent()
    agent2 = GobbletDQNAgent()
    agent1.load(model1_path)
    agent2.load(model2_path)
    agent1.epsilon = 0.0
    agent2.epsilon = 0.0
    agent_number = 0

    for line in sys.stdin:
        command = line.strip()

        if command == "CHECK_WEIGHTS":
            exists = check_weight(MODEL1_PATH) and check_weight(MODEL2_PATH)
            print("true" if exists else "false")
            sys.stdout.flush()
        elif command == "START_TRAINING_IF_NEEDED":
            exists = check_weight(MODEL1_PATH) and check_weight(MODEL2_PATH)
            if (not exists):
                model1_path = "gobblet_agent1.pth"
                model2_path = "gobblet_agent2.pth"
                trained_agent1, trained_agent2 = train_self_play(episodes=1000000)
                trained_agent1.save(model1_path)
                trained_agent2.save(model2_path)
            print("TRAINING_FINISHED")
            sys.stdout.flush()
        elif command.startswith("START_GAME"):
            env = Gobblet()
            agent_number = int(command.split()[1])
            agent1 = GobbletDQNAgent()
            agent2 = GobbletDQNAgent()
            agent1.load(model1_path)
            agent2.load(model2_path)
            print("true" if env is not None else "false")
            sys.stdout.flush()
        elif command.startswith("CHECK_TURN"):
            action = int(command.split(" ")[1])
            print("true" if action in env.get_valid_actions() else "false")
            sys.stdout.flush()
        elif command.startswith("TAKE_TURN"):
            action = int(command.split(" ")[1])
            state, reward, done = env.step(action)
            print(f"DEBUG: Human move={action}, Board={env.board}, Player={env.current_player}", file=sys.stderr)
            sys.stderr.flush()
            print(f"win {done} {reward}" if done else "continue")
            sys.stdout.flush()
        elif command == ("TAKE_AI_TURN"):
            if agent_number == 0:
                action = agent1.act(env.get_state(), env.get_valid_actions())
            else:
                action = agent2.act(env.get_state(), env.get_valid_actions())
            state, reward, done = env.step(action)
            print(f"DEBUG: AI sees Board={env.board}, Valid={env.get_valid_actions()}", file=sys.stderr)
            sys.stderr.flush()
            print(f"{action} win {done} {reward}" if done else f"{action} continue")
            sys.stdout.flush()
        elif command == "EXIT":
            break


if __name__ == "__main__":
    main()
    agent1 = GobbletDQNAgent()
    agent2 = GobbletDQNAgent()
    model1_path = "gobblet_agent1.pth"
    model2_path = "gobblet_agent2.pth"
    try:
        agent1.load(model1_path)
        agent2.load(model2_path)
        print("Загружена ранее обученная модель!")
    except FileNotFoundError:
        print("Модель не найдена. Начинаем обучение с нуля...")
        sleep(1)
        agent1, agent2 = train_self_play(episodes=1000000, checkpoint_path="checkpoints/agent1_ep910000.pt", start_episode=910000)
        agent1.save(model1_path)
        agent2.save(model2_path)
        print("Модель сохранена!")

    play_agents(agent1, agent2, games=10000)
    play_vs_random_first(agent1, games=10000)
    play_vs_random_second(agent2, games=10000)
