SR360: Boosting 360-Degree Video Streaming with Super-Resolution (Replication)This repository contains a replication of the paper SR360: Boosting 360-Degree Video Streaming with Super-Resolution (NOSSDAV 2020).The project's goal is to implement the SR360 framework described in the paper and validate its key findings—specifically, the 30% average improvement in Quality of Experience (QoE) metrics over baseline streaming methods.📄 Original PaperJiawen Chen, Miao Hu, Zhenxiao Luo, Zelong Wang and Di Wu. 2020.SR360: Boosting 360-Degree Video Streaming with Super-Resolution.In 30th Workshop on Network and Operating System Support for Digital Audio and Video (NOSSDAV '20).DOI: https://doi.org/10.1145/3386290.3396929🎯 Project GoalThe primary objective is to build a trace-driven simulator and a DRL-based streaming agent that reproduces the results from the SR360 paper. The project is divided into four main phases:Asset Collection and Preparation: Download all required video, head movement, and network datasets. Process the videos into tiled, multi-bitrate chunks.Component Implementation:SR Module: Adapt the NAS framework to train content-aware, overfitted super-resolution models for each video.DRL Streaming Agent: Build an A3C-based agent to jointly manage FoV prediction, bitrate selection, and SR enhancement decisions.Baseline and Simulation: Implement the paper's "Baseline" algorithm and develop a trace-driven simulation environment.Execution and Analysis: Run extensive simulations for both SR360 and the Baseline, comparing the resulting QoE metrics (average viewport quality, rebuffering time, and viewport quality change) against the paper's figures.🏁 Getting StartedFollow these steps to set up the environment and run the replication.PrerequisitesYou will need the following tools installed on your system:Python 3.8+FFmpeg (with libx265 support)GitInstallationClone this Repository:Bashgit clone https://github.com/[YOUR-USERNAME]/sr360-replication.git
cd sr360-replication
Clone External Dependencies:The SR360 framework is based on the Neural Adaptive Streaming (NAS) project for its super-resolution component.Bash# We will place external libraries in the `lib/` directory
mkdir lib
git clone https://github.com/kaist-ina/NAS_public.git lib/NAS_public
Set Up Python Environment:It is highly recommended to use a virtual environment.Bashpython3 -m venv venv
source venv/bin/activate
Install Python Libraries:Install all required packages using pip.Bashpip install tensorflow pandas matplotlib
# Or, if a requirements.txt is provided:
# pip install -r requirements.txt
🚀 How to Run the ReplicationThe project is executed in a sequence of steps, from data preparation to final evaluation.Phase 1: Download DatasetsBefore running any scripts, you must download the external datasets. Place them in the data/ directory.360-Degree Video Head Movement Dataset (Corbillon et al.):Link: http://dash.ipv6.enstb.fr/headMovements/Download the source videos (e.g., diving, rollerCoaster) and the head movement traces.Place them in data/video_traces/4G/LTE Measurements Dataset (van der Hooft et al.):Link: https://users.ugent.be/~jvdrhoof/dataset-4g/Download logs_all.zip.Extract and place the log files in data/network_traces/Phase 2: Prepare Video AssetsRun the video processing script. This script will:Segment source videos into 1-second chunks.Divide each frame into a $6 \times 4$ grid of tiles.Encode each tile at the five specified quality levels (130p to 540p) using FFMPEG/libx265.Bashpython src/prepare_assets.py
Note: This step is extremely time and resource-intensive. It will generate a large number of small video files.Phase 3: Train SR ModelsNext, train the content-aware SR models. This script will adapt the NAS_public code to train a unique, overfitted model for each video in the dataset.Bashpython src/train_sr.py
The trained models will be saved in the models/ directory.Phase 4: Train DRL AgentWith the simulator and SR models in place, train the DRL agent. This script will use the training traces (video and network) to teach the A3C agent how to make optimal decisions based on the paper's QoE reward formula.Bashpython src/train_drl_agent.py
The trained DRL agent policy network will be saved in models/.Phase 5: Execute and AnalyzeFinally, run the evaluation. This script will:Load the testing traces.Run the simulation for both the trained SR360 agent and the Baseline algorithm.Collect all QoE metrics (average viewport quality, rebuffering, quality change) for every session.Generate graphs and figures (e.g., CDFs) that can be directly compared to Figures 2, 3, 4, and 5 in the paper.Bashpython src/evaluate.py
The final results and plots will be saved in the results/ directory.📁 Project Structuresr360-replication/
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
├── src/                  # All project source code
│   ├── prepare_assets.py # Phase 2: Video processing pipeline
│   ├── train_sr.py       # Phase 3: SR (NAS) model training
│   ├── train_drl_agent.py# Phase 4: DRL (A3C) agent training
│   ├── evaluate.py       # Phase 5: Run final evaluation and plot results
│   ├── simulator.py      # Core trace-driven simulation environment
│   └── agents.py         # Definitions for SR360Agent and BaselineAgent
└── README.md             # You are here
📜 LicenseThis replication project is available under the MIT License. Please note that the included external libraries (NAS, Kvazaar) and datasets retain their original licenses.🙏 AcknowledgmentsTo the authors of SR360 (Jiawen Chen et al.) for their novel work.To the authors of the NAS project (Yeo et al.), which forms the basis of the SR module.To the creators of the 360-Degree Video Head Movement (Corbillon et al.) and 4G/LTE Measurements (van der Hooft et al.) datasets.