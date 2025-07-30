import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AI.env.personal_finance_env import PersonalFinanceEnv
from stable_baselines3 import PPO

# Tải mô hình đã huấn luyện
model_path = 'models/ppo_finance_agent'  # Thay bằng đường dẫn mô hình của bạn
model = PPO.load(model_path)

# Khởi tạo môi trường với dữ liệu cá nhân
env = PersonalFinanceEnv('data/synthetic_finance.csv')

# Lấy trạng thái ban đầu (tháng 8/2025)
obs = env.reset()[0]

# Dự đoán phân bổ tiền
action, _states = model.predict(obs, deterministic=True)

# Tính toán phân bổ dựa trên income
income = obs[0]  # Lấy income từ observation
allocation = {
    'essential_need': action[0] * income,
    'entertainment_need': action[1] * income,
    'saving': action[2] * income,
    'debt_payment': action[3] * income,
    'investment': action[4] * income
}

# In kết quả
print(f"Month: August 2025")
print(f"Total Income: {income:.2f} USD")
print("Allocation:")
for key, value in allocation.items():
    print(f"  {key}: {value:.2f} USD")
print(f"Action ratios: {action}")  # Hiển thị tỷ lệ

# Tùy chọn: Thực hiện bước để xem kết quả sau hành động
next_obs, reward, done, truncated, _ = env.step(action)
print(f"Reward: {reward:.2f}")
print(f"New Saving Balance: {env.saving_balance:.2f} USD")
print(f"New Debt Balance: {env.debt_balance:.2f} USD")