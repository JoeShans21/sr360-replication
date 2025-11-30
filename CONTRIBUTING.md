# Contributing / Setup Guide for Collaborators

This guide explains how to set up the **SR360-replication** project on a new machine. Since large video assets and datasets are **ignored** by git to save space, you will need to regenerate or download them locally after cloning.

## 1. Initial Setup

### Prerequisites
Ensure you have the following installed:
*   **Python 3.8+**
*   **FFmpeg** (with `libx265` support)
    *   *Mac:* `brew install ffmpeg`
    *   *Linux:* `sudo apt install ffmpeg`
*   **Git**

### Clone the Repository
```bash
git clone https://github.com/JoeShans21/sr360-replication.git
cd sr360-replication
```

### Set Up Virtual Environment
Create and activate a virtual environment to manage dependencies isolated from your system Python.
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
Install the required Python libraries (including PyTorch, TensorFlow, and NAS dependencies).
```bash
pip install -r requirements.txt
```

### Clone Submodules (NAS Library)
We use the NAS library for Super-Resolution. Clone it into `lib/`:
```bash
mkdir -p lib
git clone https://github.com/kaist-ina/NAS_public.git lib/NAS_public
```

---

## 2. Restore Local Data Assets

The `data/` directory is excluded from git. You need to populate it to run the simulator or training scripts.

### Option A: Quick Start (Synthetic Data)
If you just want to verify the code works, generate a synthetic 4K video and process it.

1.  **Generate Test Video:**
    ```bash
    mkdir -p data/video_traces/source_videos
    ffmpeg -f lavfi -i testsrc=duration=10:size=3840x2160:rate=30 -c:v libx264 -preset ultrafast -pix_fmt yuv420p data/video_traces/source_videos/test_video.mp4
    ```

2.  **Process Assets (Tile & Chunk):**
    Run the preparation script. This will create the tiled video files in `data/prepared_videos/`.
    ```bash
    # Make sure venv is active
    python prepare_assets.py
    ```

### Option B: Full Dataset (For Replication)
To replicate the paper's full results, you need the original datasets.

1.  **Download Network Traces:**
    *   Go to: `https://users.ugent.be/~jvdrhoof/dataset-4g/`
    *   Download `logs_all.zip`.
    *   Extract contents into `data/network_traces/`.

2.  **Download Head Movement Traces & Videos:**
    *   Go to: `http://dash.ipv6.enstb.fr/headMovements/`
    *   Download the specific videos referenced in the paper (e.g., RollerCoaster, Diving) and their corresponding head movement logs.
    *   Place videos in `data/video_traces/source_videos/`.
    *   Place traces in `data/video_traces/`.

3.  **Process Assets:**
    *   Update `prepare_assets.py` to point `SOURCE_VIDEO` to your downloaded video file.
    *   Run `python prepare_assets.py`.

---

## 3. Verify Installation

Run the component tests to ensure everything is working correctly.

1.  **Test Super-Resolution Module:**
    ```bash
    python src/sr_inference.py
    # Should output: "SUCCESS: Output shape matches expected 4x upscaling."
    ```

2.  **Test Simulator Skeleton:**
    ```bash
    python src/simulator.py
    # Should print initial state and step results
    ```

3.  **Test DRL Agent:**
    ```bash
    python src/agents.py
    # Should print policy output shapes
    ```

## 4. Project Status & workflow
Check `setup_summary.md` for the latest progress report and TODOs.

