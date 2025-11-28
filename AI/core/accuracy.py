import sys
import os
import pandas as pd
import numpy as np
from stable_baselines3 import PPO, A2C
from AI.env.person_loan_env import PersonalLoanEnv

# Thêm thư mục gốc của dự án vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ======== Hàm tính các metric từ log CSV ========
def compute_metrics_from_log(log_path):
    df = pd.read_csv(log_path)

    avg_reward = df['episode_reward'].mean()
    std_reward = df['episode_reward'].std()
    max_reward = df['episode_reward'].max()

    # Convergence: episode đầu tiên đạt >95% max_reward và giữ >=3 episode liên tiếp
    threshold = 0.95 * max_reward
    convergence_ep = None
    for i in range(len(df) - 2):
        if all(df['episode_reward'].iloc[i:i+3] >= threshold):
            convergence_ep = int(df['episode'].iloc[i])
            break

    mean_loss = df['loss'].mean()
    mean_steps = df['episode_steps'].mean()

    return {
        "Avg Reward": avg_reward,
        "Std Reward": std_reward,
        "Max Reward": max_reward,
        "Convergence Ep": convergence_ep,
        "Mean Loss": mean_loss,
        "Mean Steps": mean_steps
    }

# ======== Hàm tính Accuracy từ mô hình và môi trường ========
def evaluate_accuracy(model, env):
    correct = 0
    total = 0

    obs = env.reset()
    done = False
    while True:
        action, _ = model.predict(obs)
        actual = env.labels[env.current_index]
        if action == actual:
            correct += 1
        total += 1

        obs, reward, done, _ = env.step(action)
        if done:
            break

    return correct / total

# ======== Ví dụ chạy PPO ========
if __name__ == "__main__":
    env = PersonalLoanEnv('data/dataset.csv')
    model = PPO.load("models/ppo_loan_agent", env=env)

    metrics = compute_metrics_from_log("logs/reward_log_a2c.csv")
    accuracy = evaluate_accuracy(model, env)

    metrics["Accuracy"] = accuracy * 100
    print("\nPPO Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}" if isinstance(v, (int, float)) else f"{k}: {v}")
