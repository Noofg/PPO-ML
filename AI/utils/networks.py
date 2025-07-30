import torch
import torch.nn as nn

def build_mlp(input_dim, output_dim, hidden_sizes=[64, 64], activation=nn.ReLU):
    layers = []
    prev_size = input_dim
    for h in hidden_sizes:
        layers.append(nn.Linear(prev_size, h))
        layers.append(activation())
        prev_size = h
    layers.append(nn.Linear(prev_size, output_dim))
    return nn.Sequential(*layers)
