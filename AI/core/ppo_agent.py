import torch
import torch.optim as optim
from torch.distributions import Categorical
from AI.core.utils import compute_gae, normalize

class PPOAgent:
    def __init__(self, model, lr=1e-4, clip_eps=0.1, gamma=0.99, lam=0.95, n_steps=2048):
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.clip_eps = clip_eps
        self.gamma = gamma
        self.lam = lam
        self.n_steps = n_steps

    def collect_rollout(self, env, rollout_len):
        obs_list, actions, rewards, dones, log_probs, values = [], [], [], [], [], []
        obs = env.reset()
        if isinstance(obs, tuple):  
            obs = obs[0]

        for _ in range(rollout_len):
            obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)  # Thêm batch dim
            logits, value = self.model(obs_tensor)
            dist = Categorical(logits=logits)
            action = dist.sample()
            prob = torch.softmax(logits, dim=-1)[0, action.item()].item()

            next_obs, reward, done, _ = env.step(action.item())

            reward += 0.2 * (prob - 0.5)  

            obs_list.append(obs)
            actions.append(action.item())
            rewards.append(reward)
            dones.append(done)
            log_probs.append(dist.log_prob(action).detach())
            values.append(value.item())

            obs = next_obs
            if done:
                obs = env.reset()
                if isinstance(obs, tuple):
                    obs = obs[0]

        return obs_list, actions, rewards, dones, log_probs, values

    def update(self, obs_list, actions, rewards, dones, log_probs_old, values):
        # Chuẩn hóa reward theo batch (zero-mean, unit-std).
        rewards = torch.tensor(rewards, dtype=torch.float32)
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
        rewards = rewards.tolist()
# tính GAE để tạo Advantage
        advantages = compute_gae(rewards, values, dones, self.gamma, self.lam)
        returns = [a + v for a, v in zip(advantages, values)]
        advantages = normalize(advantages)

        obs_tensor = torch.tensor(obs_list, dtype=torch.float32)
        actions_tensor = torch.tensor(actions)
        returns_tensor = torch.tensor(returns, dtype=torch.float32)
        advantages_tensor = torch.tensor(advantages, dtype=torch.float32)
        log_probs_old_tensor = torch.stack(log_probs_old)

        for _ in range(15):  # epochs
            logits, value_preds = self.model(obs_tensor)
            dist = Categorical(logits=logits)
            log_probs_new = dist.log_prob(actions_tensor)

            ratio = torch.exp(log_probs_new - log_probs_old_tensor)

            surr1 = ratio * advantages_tensor
            surr2 = torch.clamp(ratio, 1 - self.clip_eps, 1 + self.clip_eps) * advantages_tensor
            policy_loss = -torch.min(surr1, surr2).mean()
            value_loss = (returns_tensor - value_preds.squeeze()).pow(2).mean()
            entropy_bonus = dist.entropy().mean()

            loss = policy_loss + 0.5 * value_loss - 0.01 * entropy_bonus

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        return loss.item()
