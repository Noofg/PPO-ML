import os
import torch
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from AI.env.person_loan_env import PersonalLoanEnv
from AI.utils.networks import ActorCriticNet
from AI.core.ppo_agent import PPOAgent

# Cấu hình
data_path = 'data/dataset.csv'
model_path = "models/ppo_personal_loan.pth"
log_path = "logs/ppo_train.csv"
os.makedirs("logs", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Load data
df = pd.read_csv(data_path)
split_idx = int(len(df) * 0.8)
train_df = df.iloc[:split_idx].reset_index(drop=True)
test_df = df.iloc[split_idx:].reset_index(drop=True)

train_df.to_csv("data/train_tmp.csv", index=False)
test_df.to_csv("data/test_tmp.csv", index=False)

# Env
env_train = PersonalLoanEnv("data/train_tmp.csv")
env_test = PersonalLoanEnv("data/test_tmp.csv")

# Model
obs_dim = env_train.observation_space.shape[0]
act_dim = env_train.action_space.n
model = ActorCriticNet(obs_dim, act_dim)

# Train
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print(f"Đã load model từ {model_path}")
else:
    agent = PPOAgent(model)
    with open(log_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["epoch", "loss", "avg_reward"])
        for epoch in range(400):
            obs_list, actions, rewards, dones, log_probs, values = agent.collect_rollout(env_train, rollout_len=512)
            loss = agent.update(obs_list, actions, rewards, dones, log_probs, values)
            loss_value = loss if loss is not None else 0.0
            avg_reward = np.mean(rewards)
            writer.writerow([epoch + 1, loss_value, avg_reward])
            print(f"Epoch {epoch+1}/400 - Loss: {loss_value:.4f} - Reward TB: {avg_reward:.3f}")
    torch.save(model.state_dict(), model_path)
    print(f"💾 Model đã được lưu vào {model_path}")

# Test
agent = PPOAgent(model)
obs_list, actions, rewards, dones, _, _ = agent.collect_rollout(env_test, rollout_len=500)
accuracy = np.mean(np.array(rewards) > 0) * 100
print(f"🎯 Test Accuracy: {accuracy:.2f}% | Reward TB: {np.mean(rewards):.3f}")

# Vẽ biểu đồ từ log
data = pd.read_csv(log_path)
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(data["epoch"], data["loss"], label="Loss per Epoch", color="red")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.subplot(1,2,2)
plt.plot(data["epoch"], data["avg_reward"], label="Reward per Epoch", color="blue")
plt.xlabel("Epoch")
plt.ylabel("Average Reward")
plt.legend()

plt.tight_layout()
plt.show()
