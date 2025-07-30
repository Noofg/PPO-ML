import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
from AI.env.personal_finance_env import PersonalFinanceEnv
from AI.env.person_loan_env import PersonalLoanEnv
from stable_baselines3 import PPO,A2C 
from AI.callback.reward_logger_callback import RewardLoggerCallback


env = PersonalLoanEnv('data/dataset.csv')
# model = PPO('MlpPolicy', env, verbose=1,learning_rate=1e-4,
#     gamma=0.99,
#     gae_lambda=0.95,
#     ent_coef=0.01,
#     vf_coef=0.4,
#     batch_size=64,
#     max_grad_norm=0.3,
#     n_steps=2048,
#     clip_range=0.1)
a2c_model = A2C("MlpPolicy", env, verbose=1, learning_rate=5e-5,
    gamma=0.98,
    gae_lambda=0.92,
    ent_coef=0.005,
    vf_coef=0.5,
    max_grad_norm=0.5)

# callback_ppo = RewardLoggerCallback(save_path='logs/reward_log_ppo.csv', verbose=1)
callback_a2c = RewardLoggerCallback(save_path='logs/a2c.csv', verbose=1)
# model.learn(total_timesteps=1000000, callback=callback_ppo)
a2c_model.learn(total_timesteps=100000, callback=callback_a2c)

a2c_model.save('models/a2c_loan_agent')
# model.save('models/ppo_loan_agent')
#model.save('models/ppo_finance_agent')

print("✅ Training done!")