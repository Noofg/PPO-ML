# AI/core/a2c_agent.py  (updated)
import os
import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
from AI.core.utils import compute_gae, normalize


class A2CAgent:
    def __init__(self, model,
                 lr=1e-4,
                 gamma=0.99,
                 lam=0.95,
                 value_coef=0.5,
                 ent_coef_start=0.05,
                 ent_coef_end=0.01,
                 max_grad_norm=0.5,
                 false_negative_penalty=1.0,
                 false_positive_penalty=0.5,
                 device=None):
      
        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
        self.model = model.to(self.device)
        # use Adam for stability
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.gamma = gamma
        self.lam = lam
        self.value_coef = value_coef
        self.ent_coef = ent_coef_start
        self.ent_coef_start = ent_coef_start
        self.ent_coef_end = ent_coef_end
        self.max_grad_norm = max_grad_norm

        # reward shaping penalties (to prefer catching positive class)
        self.fn_penalty = false_negative_penalty
        self.fp_penalty = false_positive_penalty

        # counters for annealing
        self.update_steps = 0

    def collect_n_steps(self, env, n_steps):
      
        obs_buf, actions_buf, rewards_buf, dones_buf, vals_buf = [], [], [], [], []

        obs = env.reset()
        for _ in range(n_steps):
            obs_t = torch.tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
            with torch.no_grad():
                logits, value = self.model(obs_t)            # logits: (1, A), value: (1,1)
                dist = Categorical(logits=logits)
                action = dist.sample().item()
                # probability of chosen action (for optional shaping)
                prob = torch.softmax(logits, dim=-1)[0, action].item()
                value_item = float(value.cpu().numpy()[0])

            # get true label from env if available (env.current_index points to current obs)
            true_label = None
            try:
                true_label = int(env.labels[env.current_index])
            except Exception:
                true_label = None

            next_obs, reward, done, info = env.step(int(action))

        
            reward += 0.2 * (prob - 0.5)   # small bonus for confident picks
            # cost-sensitive penalties (if we have true label)
            if true_label is not None:
                if true_label == 1 and action == 0:
                    # predicted reject while true is accept -> heavy penalty
                    reward -= self.fn_penalty
                elif true_label == 0 and action == 1:
                    # false positive (approve bad applicant) -> penalty but maybe smaller
                    reward -= self.fp_penalty

            obs_buf.append(np.array(obs, dtype=np.float32))
            actions_buf.append(int(action))
            rewards_buf.append(float(reward))
            dones_buf.append(bool(done))
            vals_buf.append(value_item)

            obs = next_obs
            if done:
                obs = env.reset()

        # bootstrap next value
        obs_t = torch.tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
        with torch.no_grad():
            _, next_value = self.model(obs_t)
            next_value = float(next_value.cpu().numpy()[0])

        return obs_buf, actions_buf, rewards_buf, dones_buf, vals_buf, next_value

    def update(self, obs_buf, actions_buf, rewards_buf, dones_buf, values_buf, next_value):
      
        # compute advantages and returns
        values = list(values_buf)
        values.append(next_value)
        advantages = compute_gae(rewards_buf, values[:-1], dones_buf, self.gamma, self.lam)
        returns = (np.array(advantages) + np.array(values[:-1])).astype(np.float32)
        advantages = normalize(advantages).astype(np.float32)

        # tensors
        obs_tensor = torch.tensor(np.array(obs_buf, dtype=np.float32), device=self.device)
        actions_tensor = torch.tensor(actions_buf, dtype=torch.int64, device=self.device)
        adv_tensor = torch.tensor(advantages, dtype=torch.float32, device=self.device)
        returns_tensor = torch.tensor(returns, dtype=torch.float32, device=self.device)

        # forward
        logits, values_pred = self.model(obs_tensor)   # logits: (N, A), values_pred: (N, 1)
        dist = Categorical(logits=logits)
        logp = dist.log_prob(actions_tensor)
        entropy = dist.entropy().mean()

        # losses
        policy_loss = -(logp * adv_tensor).mean()
        value_pred = values_pred.squeeze(-1)
        value_loss = (returns_tensor - value_pred).pow(2).mean()
        loss = policy_loss + self.value_coef * value_loss - self.ent_coef * entropy

        # optimize
        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
        self.optimizer.step()

        # anneal entropy coefficient a bit
        self.update_steps += 1
        # linear annealing from start -> end across many updates (tunable)
        frac = min(1.0, self.update_steps / 10000.0)
        self.ent_coef = self.ent_coef_start * (1 - frac) + self.ent_coef_end * frac

        return {
            "policy_loss": float(policy_loss.detach().cpu().numpy()),
            "value_loss": float(value_loss.detach().cpu().numpy()),
            "entropy": float(entropy.detach().cpu().numpy()),
            "ent_coef": float(self.ent_coef)
        }

    def save(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        torch.save(self.model.state_dict(), path)

    def load(self, path, map_location=None):
        map_location = map_location or self.device
        self.model.load_state_dict(torch.load(path, map_location=map_location))
        self.model.to(self.device)
