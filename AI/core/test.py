from stable_baselines3 import PPO
from AI.env.personal_finance_env import PersonalFinanceEnv

env = PersonalFinanceEnv('data/synthetic_finance.csv')
model = PPO.load('models/ppo_finance_agent')

obs = env.reset()
done = False
total_reward = 0
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _ = env.step(action)
    total_reward += reward

print(f"✅ Total reward: {total_reward}")
print(f"✅ Final saving balance: {env.saving_balance}")
print(f"✅ Final debt balance: {env.debt_balance}")
