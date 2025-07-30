import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AI.env.person_loan_env import PersonalLoanEnv

env = PersonalLoanEnv('data/dataset.csv')

max_timesteps = 100_000
timestep_count = 0
results = []
episode = 0

def rule_based_action(observation):
    try:
        income = observation.get("income", 0)
        essential = observation.get("essential_need", 0)
        entertainment = observation.get("entertainment_need", 0)
        unexpected = observation.get("unexpected_expense", 0)

        total_expense = essential + entertainment + unexpected

        if income > total_expense:
            return 1  # đầu tư
        else:
            return 0  # không đầu tư
    except Exception as e:
        return env.action_space.sample()  # fallback nếu có lỗi


while timestep_count < max_timesteps:
    obs = env.reset()
    done = False
    total_reward = 0
    steps = 0
    episode += 1

    while not done:
        action = rule_based_action(obs)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        steps += 1
        timestep_count += 1

        if timestep_count >= max_timesteps:
            break

    final_saving = info.get("final_saving_balance", None)
    results.append({
        'episode': episode,
        'episode_reward': total_reward,
        'final_saving_balance': final_saving,
        'episode_steps': steps
    })

# Lưu kết quả
df = pd.DataFrame(results)
os.makedirs("logs", exist_ok=True)
df.to_csv("logs/rule_based.csv", index=False)
print(f" Rule-based agent done after {timestep_count} timesteps. Log saved to logs/rule_based.csv")
