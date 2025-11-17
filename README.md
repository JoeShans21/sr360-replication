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

Follow these steps to set up the environment and run the replication.

### Prerequisites

You will need the following tools installed on your system:

* Python 3.8+
* [FFmpeg](https://ffmpeg.org/download.html) (with `libx265` support)
* [Git](https://git-scm.com/downloads)

### Installation

1.  **Clone this Repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR-USERNAME]/sr360-replication.git
    cd sr360-replication
    ```

2.  **Clone External Dependencies:**
    The SR360 framework is based on the Neural Adaptive Streaming (NAS) project for its super-resolution component.
    ```bash
    # We will place external libraries in the `lib/` directory
    mkdir lib
    git clone [https://github.com/kaist-ina/NAS_public.git](https://github.com/kaist-ina/NAS_public.git) lib/NAS_public
    ```

3.  **Set Up Python Environment:**
    It is highly recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Python Libraries:**
    Install all required packages using `pip`.
    ```bash
    pip install tensorflow pandas matplotlib
    # Or, if a requirements.txt is provided:
    # pip install -r requirements.txt
    ```

## 🚀 How to Run the Replication

The project is executed in a sequence of steps, from data preparation to final evaluation.

### Phase 1: Download Datasets

Before running any scripts, you must download the external datasets. Place them in the `data/` directory.

1.  **360-Degree Video Head Movement Dataset (Corbillon et al.):**
    * **Link:** `http://dash.ipv6.enstb.fr/headMovements/`
    * Download the source videos (e.g., `diving`, `rollerCoaster`) and the head movement traces.
    * Place them in `data/video_traces/`

2.  **4G/LTE Measurements Dataset (van der Hooft et al.):**
    * **Link:** `https://users.ugent.be/~jvdrhoof/dataset-4g/`
    * Download `logs_all.zip`.
    * Extract and place the log files in `data/network_traces/`
