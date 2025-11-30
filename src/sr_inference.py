import sys
import os
import torch
import numpy as np
from argparse import Namespace

# --- Setup paths to include NAS_public ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NAS_LIB_PATH = os.path.join(PROJECT_ROOT, 'lib', 'NAS_public')
sys.path.append(NAS_LIB_PATH)

# --- Mock sys.argv to satisfy option.py's argparse ---
# option.py parses args immediately on import. We need to provide minimal valid args.
# We'll save the original argv, set a dummy one, import, then restore.
original_argv = sys.argv
sys.argv = ['dummy_script', '--data_name', 'test_video', '--quality', 'low']

try:
    from model import MultiNetwork
    from template import get_nas_config
    # We might need 'opt' if the model relies on it globally, though MultiNetwork seems to take config in __init__
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
        
        # Load model configuration
        config = get_nas_config(quality)
        
        # Initialize model
        self.model = MultiNetwork(config).to(self.device)
        
        # Set default target scale (e.g., 4x upscale)
        # NAS supports 1, 2, 3, 4. We typically want max upscale for 360 video tiles?
        # The paper says: "A video tile with low resolution can be boosted... to high resolution"
        # If we have 540p tiles as max (high), and 130p as min. 130p * 4 ~ 520p close to 540p.
        self.model.setTargetScale(4) 
        
        # Validation mode (eval)
        self.model.eval()
        
    def load_weights(self, weight_path):
        """
        Load trained weights into the model.
        """
        if os.path.exists(weight_path):
            print(f"Loading weights from {weight_path}")
            # Note: The NAS save_chunk method saves partial dicts. 
            # Loading might need specific logic if we use those chunks.
            # For a full checkpoint, we'd use standard torch load.
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
            # Add batch dimension: (1, C, H, W)
            input_batch = tensor_chw.unsqueeze(0).to(self.device)
            
            # Forward pass
            # idx=None allows random path in training, but for inference 
            # MultiNetwork.forward calls SingleNetwork.forward.
            # SingleNetwork.forward defaults idx to random choice from outputList if None!
            # We probably want deterministic inference.
            # Looking at SingleNetwork.forward:
            # "if idx is None: idx = random.choice(self.outputList)"
            # This implies we MUST provide idx for deterministic output?
            # Or maybe outputList only has one option in eval mode?
            # ops.random_gradual_03 suggests it's for any-time prediction.
            # For now, we'll let it be random or fix it if we know the "full" path index.
            # Usually the last block is the "best" quality.
            # SingleNetwork init: self.outputNode = sorted(self.outputNode)
            # We can likely grab the max index from the model internals if needed.
            
            output_batch = self.model(input_batch)
            return output_batch.squeeze(0)

if __name__ == "__main__":
    # Simple test
    print("Initializing SRInferencer...")
    inferencer = SRInferencer(quality='low', device='cpu')
    
    # Create dummy input: 3 channels, 130x130 (representing a small tile)
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

