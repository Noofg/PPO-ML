import sys
import os
import time
import pandas as pd
from sklearn.model_selection import train_test_split
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AI.env.person_loan_env import PersonalLoanEnv
from stable_baselines3 import PPO, A2C
from AI.callback.reward_logger_callback import RewardLoggerCallback

# Hàm chia dataset
def split_dataset(csv_path, train_ratio=0.8, random_state=42):
    data = pd.read_csv(csv_path)
    train_data, test_data = train_test_split(data, train_size=train_ratio, random_state=random_state)
    return train_data, test_data

# Hàm đánh giá model
def evaluate_model(model, env, num_episodes=100):
    total_rewards = []
    for _ in range(num_episodes):
        reset_result = env.reset()
        if isinstance(reset_result, tuple):
            obs = reset_result[0]
        else:
            obs = reset_result

        done = False
        episode_reward = 0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            step_result = env.step(action)

            # Xử lý tương thích Gym mới / cũ
            if len(step_result) == 5:
                obs, reward, terminated, truncated, _ = step_result
                done = terminated or truncated
            else:
                obs, reward, done, _ = step_result

            episode_reward += reward
        total_rewards.append(episode_reward)

    avg_reward = sum(total_rewards) / len(total_rewards)
    std_reward = (sum((r - avg_reward) ** 2 for r in total_rewards) / len(total_rewards)) ** 0.5
    return avg_reward, std_reward, max(total_rewards)

# Hàm tính tốc độ hội tụ
def get_convergence_episode(log_csv, threshold_ratio=0.95):
    df = pd.read_csv(log_csv)
    max_reward = df['episode_reward'].max()
    threshold = threshold_ratio * max_reward
    try:
        ep = df[df['episode_reward'] >= threshold].index[0] + 1
    except IndexError:
        ep = None
    return ep

# Main
csv_path = 'data/dataset.csv'
train_data, test_data = split_dataset(csv_path, train_ratio=0.8)

train_csv = 'data/train.csv'
test_csv = 'data/test.csv'
train_data.to_csv(train_csv, index=False)
test_data.to_csv(test_csv, index=False)

train_env = PersonalLoanEnv(train_csv) 
test_env = PersonalLoanEnv(test_csv)

# Model configs
ppo_model = PPO(
    'MlpPolicy', train_env, verbose=1, learning_rate=1e-4,
    gamma=0.99, gae_lambda=0.95, ent_coef=0.01, vf_coef=0.4,
    batch_size=64, max_grad_norm=0.3, n_steps=2048, clip_range=0.1
)
a2c_model = A2C(
    'MlpPolicy', train_env, verbose=1, learning_rate=5e-5,
    gamma=0.99, gae_lambda=0.95, ent_coef=0.01, vf_coef=0.4,
    max_grad_norm=0.5
)

# Callbacks log reward
ppo_log_path = 'logs/reward_log_ppo.csv'
a2c_log_path = 'logs/reward_log_a2c.csv'
callback_ppo = RewardLoggerCallback(save_path=ppo_log_path, verbose=1)
callback_a2c = RewardLoggerCallback(save_path=a2c_log_path, verbose=1)

# Train PPO
print("Training PPO...")
start_ppo = time.time()
ppo_model.learn(total_timesteps=100000, callback=callback_ppo)
end_ppo = time.time()
ppo_model.save('models/ppo_loan_agent')

# Train A2C
print("Training A2C...")
start_a2c = time.time()
a2c_model.learn(total_timesteps=100000, callback=callback_a2c)
end_a2c = time.time()
a2c_model.save('models/a2c_loan_agent')

# Evaluate
ppo_avg, ppo_std, ppo_max = evaluate_model(ppo_model, test_env)
a2c_avg, a2c_std, a2c_max = evaluate_model(a2c_model, test_env)

# Convergence episodes
ppo_conv = get_convergence_episode(ppo_log_path)
a2c_conv = get_convergence_episode(a2c_log_path)

# Tổng hợp kết quả
results = pd.DataFrame({
    "Model": ["PPO", "A2C"],
    "Avg Reward": [ppo_avg, a2c_avg],
    "Std Reward": [ppo_std, a2c_std],
    "Max Reward": [ppo_max, a2c_max],
    "Convergence Ep": [ppo_conv, a2c_conv],
    "Training Time (s)": [end_ppo - start_ppo, end_a2c - start_a2c]
})

print("\n===== Performance Comparison =====")
print(results.to_string(index=False))

# Lưu bảng kết quả
results.to_csv("logs/performance_comparison.csv", index=False)
print("✅ Training and evaluation done! Results saved to logs/performance_comparison.csv")
