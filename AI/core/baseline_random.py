import sys
import os
import pandas as pd

# Đảm bảo import được PersonalLoanEnv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env.person_loan_env import PersonalLoanEnv


def run_random_agent(env, max_timesteps=100_000, log_path="logs/baseline_random.csv"):
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
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv(log_path, index=False)
    print(f"✅ Baseline random agent done after {timestep_count} timesteps. Log saved to {log_path}")


if __name__ == "__main__":
    env = PersonalLoanEnv('data/dataset.csv')
    run_random_agent(env, max_timesteps=100_000, log_path="logs/baseline_random.csv")
