import sys
import os
import torch
import numpy as np
from argparse import Namespace

# Add NAS_public to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NAS_LIB_PATH = os.path.join(PROJECT_ROOT, 'lib', 'NAS_public')
sys.path.append(NAS_LIB_PATH)

# Fake sys.argv to avoid option.py's argparse crash on import
# Save real argv, swap in dummy one, then put back after import.
original_argv = sys.argv
sys.argv = ['dummy_script', '--data_name', 'test_video', '--quality', 'low']

try:
    from model import MultiNetwork
    from template import get_nas_config
    # 'opt' may be used as a global config in the NAS code
    from option import opt as nas_opt 
except ImportError as e:
    print(f"Error importing NAS modules: {e}")
    sys.exit(1)
finally:
    sys.argv = original_argv


class SRInferencer:
    def __init__(self, quality='low', device='cpu'):
        """
        Initialize the SR model.
        
        Args:
            quality (str): 'low', 'medium', 'high', 'ultra'
            device (str): 'cpu' or 'cuda'
        """
        self.device = torch.device(device)
        self.quality = quality
        
        # Load NAS model config
        config = get_nas_config(quality)
        
        # Initialize NAS model
        self.model = MultiNetwork(config).to(self.device)
        
        # Use 4x upscaling by default (NAS supports integer scales 1-4).
        # For our tiles, 4x roughly maps the low-res tiles back to the target resolution.
        self.model.setTargetScale(4) 
        
        # Set model to evaluation mode
        self.model.eval()
        
    def load_weights(self, weight_path):
        """
        Load trained weights into the model.
        """
        if os.path.exists(weight_path):
            print(f"Loading weights from {weight_path}")
            # save_chunk writes partial state_dicts; loading those may need extra handling.
            checkpoint = torch.load(weight_path, map_location=self.device)
            self.model.load_state_dict(checkpoint)
        else:
            print(f"Warning: Weight file {weight_path} not found. Using random weights.")

    def upscale(self, tensor_chw):
        """
        Upscale a tensor (C, H, W).
        
        Args:
            tensor_chw (torch.Tensor): Input tensor, normalized 0-1 usually? 
                                       NAS dataset.py uses ToTensor() which is 0-1.
        Returns:
            torch.Tensor: Upscaled tensor (C, H*scale, W*scale)
        """
        with torch.no_grad():
            # Aqdd batch dimension: (1, C, H, W)
            input_batch = tensor_chw.unsqueeze(0).to(self.device)
            
            # Forward pass (uses default NAS inference path internally).
            output_batch = self.model(input_batch)
            return output_batch.squeeze(0)

if __name__ == "__main__":
    # Simple test
    print("Initializing SRInferencer...")
    inferencer = SRInferencer(quality='low', device='cpu')
    
    dummy_input = torch.rand(3, 130, 130)
    print(f"Input shape: {dummy_input.shape}")
    
    output = inferencer.upscale(dummy_input)
    print(f"Output shape: {output.shape}")
    
    # Check scaling
    scale = 4
    expected_shape = (3, 130*scale, 130*scale)
    if output.shape == expected_shape:
        print("SUCCESS: Output shape matches expected 4x upscaling.")
    else:
        print(f"FAILURE: Expected {expected_shape}, got {output.shape}")

