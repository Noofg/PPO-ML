import torch
import torch.nn as nn
import torch.nn.functional as F

class ActorCritic(nn.Module):
    def __init__(self, obs_dim, action_dim, hidden_dim=128):
        super().__init__()
        # shared backbone
        self.fc1 = nn.Linear(obs_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)

        # actor head (logits for Categorical)
        self.actor = nn.Linear(hidden_dim, action_dim)

        # critic head (scalar)
        self.critic = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        # Accept numpy arrays or torch tensors
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x, dtype=torch.float32)
        if x.dim() == 1:
            x = x.unsqueeze(0)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        logits = self.actor(x)
        value = self.critic(x).squeeze(-1)
        return logits, value
