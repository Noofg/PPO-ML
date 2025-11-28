import os
import time
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

from AI.env.person_loan_env import PersonalLoanEnv
from AI.utils.networks import ActorCriticNet
from AI.core.a2c_agent import A2CAgent

data_path = 'data/dataset.csv'
df = pd.read_csv(data_path)

split_idx = int(len(df) * 0.8)
train_df = df.iloc[:split_idx].reset_index(drop=True)
test_df = df.iloc[split_idx:].reset_index(drop=True)

env_train = PersonalLoanEnv("data/train_tmp.csv")
env_test = PersonalLoanEnv("data/test_tmp.csv")

obs_dim = env_train.observation_space.shape[0]
act_dim = env_train.action_space.n
model = ActorCriticNet(obs_dim, act_dim) 

model_path = "models/a2c_personal_loan.pth"

if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print(f"Đã load model từ {model_path}")
else:
    agent = A2CAgent(model, lr=1e-4)

    for epoch in range(400):
        # Thu thập dữ liệu n bước
        obs_buf, actions_buf, rewards_buf, dones_buf, vals_buf, next_value = \
            agent.collect_n_steps(env_train, n_steps=2048)

        # Cập nhật A2C
        stats = agent.update(obs_buf, actions_buf, rewards_buf, dones_buf, vals_buf, next_value)

        print(f"Epoch {epoch+1}/400 | "
              f"Policy Loss: {stats['policy_loss']:.4f} | "
              f"Value Loss: {stats['value_loss']:.4f} | "
              f"Entropy: {stats['entropy']:.4f} | "
              f"Reward TB: {np.mean(rewards_buf):.3f}")

    # Lưu model
    torch.save(model.state_dict(), model_path)
    print(f"💾 Model đã được lưu vào {model_path}")

# Test
agent = A2CAgent(model, lr=1e-4)
obs_buf, actions_buf, rewards_buf, dones_buf, vals_buf, next_value = \
    agent.collect_n_steps(env_test, n_steps=2048)

accuracy = np.mean(np.array(rewards_buf) > 0) * 100
print(f"Test Accuracy: {accuracy:.2f}% | Reward TB: {np.mean(rewards_buf):.3f}")
