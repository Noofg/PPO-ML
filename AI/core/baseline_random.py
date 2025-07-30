import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AI.env.person_loan_env import PersonalLoanEnv

env = PersonalLoanEnv('data/dataset.csv')

max_timesteps = 100_000  # tổng số bước (không phải số episode)
timestep_count = 0
results = []
episode = 0

while timestep_count < max_timesteps:
    obs = env.reset()
    done = False
    total_reward = 0
    steps = 0
    episode += 1

    while not done:
        action = env.action_space.sample()  # random action
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

# Lưu log vào file CSV
df = pd.DataFrame(results)
os.makedirs("logs", exist_ok=True)
df.to_csv("logs/baseline_random.csv", index=False)
print(f"✅ Baseline random agent done after {timestep_count} timesteps. Log saved to logs/baseline_random.csv")
