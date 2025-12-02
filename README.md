# SR360: Boosting 360-Degree Video Streaming with Super-Resolution (Replication)

This repository contains a replication of the paper **SR360: Boosting 360-Degree Video Streaming with Super-Resolution** (NOSSDAV 2020).

The project's goal is to implement the SR360 framework described in the paper and validate its key findings—specifically, the 30% average improvement in Quality of Experience (QoE) metrics over baseline streaming methods.

## 📄 Original Paper

> Jiawen Chen, Miao Hu, Zhenxiao Luo, Zelong Wang and Di Wu. 2020.
> **SR360: Boosting 360-Degree Video Streaming with Super-Resolution.**
> In *30th Workshop on Network and Operating System Support for Digital Audio and Video (NOSSDAV '20).*
>
> **DOI:** `https://doi.org/10.1145/3386290.3396929`

## 🎯 Project Goal

The primary objective is to build a trace-driven simulator and a DRL-based streaming agent that reproduces the results from the SR360 paper. The project is divided into four main phases:

1.  **Asset Collection and Preparation:** Download all required video, head movement, and network datasets. Process the videos into tiled, multi-bitrate chunks.
2.  **Component Implementation:**
    * **SR Module:** Adapt the NAS framework to train content-aware, overfitted super-resolution models for each video.
    * **DRL Streaming Agent:** Build an A3C-based agent to jointly manage FoV prediction, bitrate selection, and SR enhancement decisions.
3.  **Baseline and Simulation:** Implement the paper's "Baseline" algorithm and develop a trace-driven simulation environment.
4.  **Execution and Analysis:** Run extensive simulations for both SR360 and the Baseline, comparing the resulting QoE metrics (average viewport quality, rebuffering time, and viewport quality change) against the paper's figures.

## 🏁 Getting Started

**Collaborators:** Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed setup instructions, including how to regenerate local data assets not included in the git repo.

Follow these steps to set up the environment and run the replication.

### Prerequisites

You will need the following tools installed on your system:

* Python 3.8+
* [FFmpeg](https://ffmpeg.org/download.html) (with `libx265` support)
* [Git](https://git-scm.com/downloads)

### Installation

1.  **Clone this Repository:**
    ```bash
    git clone https://github.com/JoeShans21/sr360-replication
    cd sr360-replication
    ```

2.  **Clone External Dependencies:**
    The SR360 framework is based on the Neural Adaptive Streaming (NAS) project for its super-resolution component.
    ```bash
    # We will place external libraries in the `lib/` directory
    mkdir lib
    git clone https://github.com/kaist-ina/NAS_public.git lib/NAS_public
    ```

3.  **Set Up Python Environment:**
    It is highly recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Python Libraries:**
    Install all required packages using `pip` and the provided `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 How to Run the Replication

The project is executed in a sequence of steps, from data preparation to final evaluation.

### Phase 1: Download Datasets

Before running any scripts, you must obtain the datasets. Place them in the `data/` directory.

1.  **360-Degree Video Head Movement Dataset (Corbillon et al.):**
    * **Link:** `https://tinyurl.com/3brdmm4s`
    * Download the source videos (e.g., `diving`, `rollerCoaster`) and the head movement traces.
    * Place them in `data/video_traces/`

2.  **4G/LTE Measurements Dataset (van der Hooft et al.):**
    * **Link:** `https://users.ugent.be/~jvdrhoof/dataset-4g/`
    * Download `logs_all.zip`.
    * Extract and place the log files in `data/network_traces/`

**Alternative: Synthetic Test Video Generation**
If you cannot download the datasets immediately, you can generate a synthetic 4K test video for verification:
```bash
mkdir -p data/video_traces/source_videos
ffmpeg -f lavfi -i testsrc=duration=10:size=3840x2160:rate=30 -c:v libx264 -preset ultrafast -pix_fmt yuv420p data/video_traces/source_videos/test_video.mp4
```

### Phase 2: Prepare Video Assets

Run the video processing script. This script will:
1.  Segment source videos into 1-second chunks.
2.  Divide each frame into a $6 \times 4$ grid of tiles.
3.  Encode each tile at the five specified quality levels (130p to 540p) using FFMPEG/libx265.

```bash
python prepare_assets.py
```
*Note: This step is extremely time and resource-intensive. It will generate a large number of small video files.*

### Phase 3: Train SR Models
*Coming soon...*
(Adapt the NAS_public code to train a unique, overfitted model for each video in the dataset.)

### Phase 4: Train DRL Agent
*Coming soon...*
(Train the A3C agent to make optimal decisions based on the paper's QoE reward formula.)

### Phase 5: Execute and Analyze
*Coming soon...*
(Run the simulation for both the trained SR360 agent and the Baseline algorithm.)

## 📁 Project Structure

```
sr360-replication/
├── config/               # Configuration files
├── data/                 # Raw and prepared datasets
│   ├── network_traces/     # 4G/LTE logs
│   ├── video_traces/       # Head movement data and source videos
│   └── prepared_videos/    # Output of prepare_assets.py
├── lib/                  # External code (git submodules)
│   └── NAS_public/       # Cloned NAS repository
├── models/               # Saved SR and DRL models
│   ├── sr/               # Trained content-aware SR models
│   └── drl/              # Trained DRL agent policy
├── results/              # Output graphs and logs from evaluation
├── prepare_assets.py     # Phase 2: Video processing pipeline
├── video_downloads.py    # Phase 1: Video download script
└── README.md             # You are here
```

## 📜 License
This replication project is available under the MIT License. Please note that the included external libraries (NAS) and datasets retain their original licenses.

## 🙏 Acknowledgments
To the authors of SR360 (Jiawen Chen et al.) for their novel work.
To the authors of the NAS project (Yeo et al.), which forms the basis of the SR module.
To the creators of the 360-Degree Video Head Movement (Corbillon et al.) and 4G/LTE Measurements (van der Hooft et al.) datasets.
