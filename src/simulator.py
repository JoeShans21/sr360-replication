import os
import pandas as pd
import numpy as np
import glob

class NetworkTrace:
    def __init__(self, trace_path):
        self.trace_path = trace_path
        self.data = self._load_trace(trace_path)
        self.ptr = 0
        
    def _load_trace(self, path):
        """
        Load 4G/LTE log file.
        Format assumption based on sample:
        Timestamp Duration Lat Lon Bytes Type?
        1452002003586 840 ... 1766452 840
        """
        if not os.path.exists(path):
            print(f"Warning: Trace {path} not found. Using mock.")
            return pd.DataFrame({'throughput': [5.0] * 1000}) # 5 Mbps mock

        try:
            # Read space-separated values
            df = pd.read_csv(path, sep='\s+', header=None, names=['ts', 'duration', 'lat', 'lon', 'bytes', 'col6'])
            
            # Convert bytes/duration to Mbps
            # throughput (Mbps) = (bytes * 8) / (duration / 1000) / 1,000,000
            df['throughput_mbps'] = (df['bytes'] * 8) / (df['duration'] / 1000.0) / 1e6
            
            return df[['ts', 'throughput_mbps']]
        except Exception as e:
            print(f"Error loading trace {path}: {e}")
            return pd.DataFrame({'throughput': [5.0] * 1000})

    def get_throughput(self):
        """Return throughput for the current step in Mbps"""
        if self.ptr >= len(self.data):
            self.ptr = 0 # Loop trace
            
        tp = self.data.iloc[self.ptr]['throughput_mbps']
        self.ptr += 1
        return tp

class VideoLibrary:
    def __init__(self, video_base_dir):
        self.base_dir = video_base_dir
        # Structure: video_name -> chunk_idx -> tile_row -> tile_col -> bitrate -> size
        self.videos = {}
        self._scan_library()
        
    def _scan_library(self):
        """
        Scans the directory for prepared videos.
        Expected: data/prepared_videos/{video_name}/chunk_{iii}/tile_{r}_{c}/{bitrate}.mp4
        """
        if not os.path.exists(self.base_dir):
            print(f"Warning: Video dir {self.base_dir} not found.")
            return

        # Walk through video directories
        for video_name in os.listdir(self.base_dir):
            video_path = os.path.join(self.base_dir, video_name)
            if not os.path.isdir(video_path):
                continue
                
            self.videos[video_name] = {}
            
            # Find chunks
            # Structure update: The prepare_assets.py script outputs:
            # .../chunk_000/tile_0_0/1M.mp4
            # It seems it puts them directly under video_name/chunk_...
            # Let's verify with glob
            
            # Pattern: video/chunk_*/tile_*/*.mp4
            chunk_dirs = glob.glob(os.path.join(video_path, "chunk_*"))
            
            for chunk_path in chunk_dirs:
                chunk_name = os.path.basename(chunk_path)
                try:
                    chunk_idx = int(chunk_name.split('_')[1])
                except ValueError:
                    continue
                    
                self.videos[video_name][chunk_idx] = {}
                
                tile_dirs = glob.glob(os.path.join(chunk_path, "tile_*_*"))
                for tile_path in tile_dirs:
                    tile_name = os.path.basename(tile_path)
                    # tile_0_0 -> row 0, col 0
                    parts = tile_name.split('_')
                    row, col = int(parts[1]), int(parts[2])
                    
                    if row not in self.videos[video_name][chunk_idx]:
                        self.videos[video_name][chunk_idx][row] = {}
                    
                    self.videos[video_name][chunk_idx][row][col] = {}
                    
                    # Get file sizes for bitrates
                    mp4_files = glob.glob(os.path.join(tile_path, "*.mp4"))
                    for mp4 in mp4_files:
                        bitrate_str = os.path.splitext(os.path.basename(mp4))[0] # "1M"
                        size_bits = os.path.getsize(mp4) * 8
                        self.videos[video_name][chunk_idx][row][col][bitrate_str] = size_bits

    def get_tile_size(self, video, chunk, row, col, bitrate):
        """Return size in bits"""
        try:
            return self.videos[video][chunk][row][col][bitrate]
        except KeyError:
            # Fallback or missing data
            return 1000 * 8 # Mock 1KB

class VideoSession:
    def __init__(self, video_name, video_lib, tiling_grid=(6, 4), chunk_duration=1):
        self.video_name = video_name
        self.video_lib = video_lib
        self.tiling_grid = tiling_grid
        self.chunk_duration = chunk_duration
        self.buffer_level = 0.0
        self.playback_ptr = 0 # Current chunk index
        
    def step(self, downloaded_bits, throughput_mbps):
        """
        Advance simulation by downloading one chunk's worth of tiles.
        """
        # Calculate download time
        if throughput_mbps <= 0: throughput_mbps = 0.1
        
        download_time = downloaded_bits / (throughput_mbps * 1e6) # bits / bps = seconds
        
        # Buffer update: add chunk duration, subtract download time
        # But logically: We consume buffer while downloading.
        # If buffer < download_time, we rebuffer.
        
        drain = download_time
        
        if self.buffer_level >= drain:
            self.buffer_level -= drain
            rebuf = 0
        else:
            rebuf = drain - self.buffer_level
            self.buffer_level = 0
            
        # Add the new chunk to buffer (now available for playback)
        self.buffer_level += self.chunk_duration
        
        self.playback_ptr += 1
        
        return rebuf, download_time

class Environment:
    def __init__(self, trace_path, video_name, video_base_dir="data/prepared_videos"):
        self.net_trace = NetworkTrace(trace_path)
        self.video_lib = VideoLibrary(video_base_dir)
        self.video_name = video_name
        self.video_session = VideoSession(video_name, self.video_lib)
        
    def get_state(self):
        # Return state vector: (Rk, Bk, xk, dk, fovk, vpk, ck)
        # Placeholder values for now
        return np.zeros(7)
        
    def step(self, action):
        # Action: (viewport_tile_idx, bitrates_dict, sr_map)
        # simplified for testing: action is just a dict of {tile_idx: bitrate}
        
        # 1. Determine tiles to download
        # For now, assume we download ALL tiles (simplification) or specific ones
        # Let's assume action specifies bitrate for all 24 tiles
        
        total_bits = 0
        chunk_idx = self.video_session.playback_ptr
        
        # Mock iteration over all tiles
        rows, cols = 6, 4 # based on paper
        # Note: prepare_assets uses 6 cols, 4 rows? or 6 rows 4 cols?
        # prepare_assets: TILES_GRID = (6, 4) -> col=6, row=4
        rows, cols = 4, 6 
        
        for r in range(rows):
            for c in range(cols):
                # Default to '1M' if not specified
                bitrate = '1M' 
                size = self.video_lib.get_tile_size(self.video_name, chunk_idx, r, c, bitrate)
                total_bits += size
        
        # 2. Get network throughput
        tp = self.net_trace.get_throughput()
        
        # 3. Simulate download
        rebuf, dl_time = self.video_session.step(total_bits, tp)
        
        # 4. Reward
        reward = -rebuf # Simple rebuffer penalty
        
        next_state = self.get_state()
        done = False # TODO check max chunks
        
        info = {
            'throughput': tp,
            'rebuffer': rebuf,
            'dl_time': dl_time,
            'chunk_idx': chunk_idx
        }
        return next_state, reward, done, info

if __name__ == "__main__":
    print("Initializing Simulator with Real Data...")
    
    # Point to a real trace if available, else mock
    trace_file = "data/network_traces/report_bicycle_0001.log"
    
    env = Environment(trace_file, "test_video")
    
    print(f"Trace loaded. Initial Throughput: {env.net_trace.get_throughput()} Mbps")
    
    # Test file size loading
    # Check if test_video loaded
    if "test_video" in env.video_lib.videos:
        print(f"Video 'test_video' loaded. Chunk 0 sizes: {len(env.video_lib.videos['test_video'].get(0, {}))} rows.")
    else:
        print("Video 'test_video' not found in library. (Did you run prepare_assets.py?)")

    # Step
    print("Stepping environment...")
    state, reward, done, info = env.step(None)
    print(f"Result: {info}")
