import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

class ActorCritic(nn.Module):
    def __init__(self, state_dim, action_dim_viewport, action_dim_bitrate):
        super(ActorCritic, self).__init__()
        
        # Simple MLP feature extractor
        self.feature_layer = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )
        
        # Actor heads
        # 1. Viewport: which tile is center
        self.actor_viewport = nn.Linear(128, action_dim_viewport)
        
        # 2. Bitrate: quality level for tiles in viewport
        self.actor_bitrate = nn.Linear(128, action_dim_bitrate)
        
        # 3. SR decision: turn super-resolution on/off
        self.actor_sr = nn.Linear(128, 2) 
        
        # Critic Head
        self.critic = nn.Linear(128, 1)
        
    def forward(self, state):
        features = self.feature_layer(state)
        
        # Policies
        pi_viewport = F.softmax(self.actor_viewport(features), dim=-1)
        pi_bitrate = F.softmax(self.actor_bitrate(features), dim=-1)
        pi_sr = F.softmax(self.actor_sr(features), dim=-1)
        
        # Value
        value = self.critic(features)
        
        return pi_viewport, pi_bitrate, pi_sr, value

if __name__ == "__main__":
    print("Initializing DRL Agent...")
    # Mock dims: 
    # State: 7 (from simulator.py placeholder)
    # Viewport: 24 tiles (6x4)
    # Bitrate: 5 levels
    model = ActorCritic(7, 24, 5)
    
    dummy_state = torch.randn(1, 7)
    pi_vp, pi_br, pi_sr, val = model(dummy_state)
    
    print(f"Viewport Policy Shape: {pi_vp.shape}")
    print(f"Bitrate Policy Shape: {pi_br.shape}")
    print(f"SR Policy Shape: {pi_sr.shape}")
    print(f"Value: {val.item()}")

