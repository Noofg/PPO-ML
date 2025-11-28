from stable_baselines3 import PPO
from AI.env.person_loan_env import PersonalLoanEnv
from AI.core.rule_based import rule_based_action
from AI.core.baseline_random import run_random_agent

env = PersonalLoanEnv('data/dataset.csv')
model = PPO.load('models/ppo_loan_agent')

obs = env.reset()
done = False
total_reward = 0
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _ = env.step(action)
    total_reward += reward

print(f" Total reward: {total_reward}")
print(f" Final saving balance: {env.labels}")
 
print("Running Random Policy")
random_rewards = run_random_agent(env, num_episodes=20)

print("\n▶Running Rule-Based Policy")
rule_rewards = rule_based_action(env, num_episodes=20)
