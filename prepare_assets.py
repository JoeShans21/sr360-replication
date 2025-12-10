import os
import subprocess

# Config
SOURCE_VIDEO = "data/video_traces/source_videos/grand.mp4"
OUTPUT_DIR = "data/prepared_videos/grand"
CHUNK_DURATION = 1  # 1 sec
TILES_GRID = (6, 4)  # 6x4
BITRATES = ["1M", "2M", "4M", "6M", "8M"]  # 1, 2, 4, 6, 8 Mbps
# 4K video split into a 6x4 tile grid
TILE_WIDTH = 3840 // TILES_GRID[0]  # 3840 / 6 = 640
TILE_HEIGHT = 2160 // TILES_GRID[1]  # 2160 / 4 = 540

# Step 1: Segment video into 1-second chunks without re-encoding
chunk_dir = os.path.join(OUTPUT_DIR, "chunks")
os.makedirs(chunk_dir, exist_ok=True)
segment_command = [
    "ffmpeg",
    "-i",
    SOURCE_VIDEO,
    "-f",
    "segment",
    "-segment_time",
    str(CHUNK_DURATION),
    "-c",
    "copy",
    "-reset_timestamps",
    "1",
    "-map",
    "0",
    os.path.join(chunk_dir, "chunk_%03d.mp4"),
]
# print(f"Running: {' '.join(segment_command)}")
subprocess.run(segment_command, check=True)
print(f"Video segmented into chunks in {chunk_dir}")

# Step 2: Loop through chunks, create all tiles and bitrates
chunk_files = sorted([f for f in os.listdir(chunk_dir) if f.endswith(".mp4")])

for chunk_file in chunk_files:
    chunk_name = os.path.splitext(chunk_file)[0]
    chunk_path = os.path.join(chunk_dir, chunk_file)

    for row in range(TILES_GRID[1]):
        for col in range(TILES_GRID[0]):

            x_pos = col * TILE_WIDTH
            y_pos = row * TILE_HEIGHT

            # Cut out one tile
            crop_filter = f"crop={TILE_WIDTH}:{TILE_HEIGHT}:{x_pos}:{y_pos}"

            for bitrate in BITRATES:
                # Create final output directory
                tile_output_dir = os.path.join(
                    OUTPUT_DIR, chunk_name, f"tile_{row}_{col}"
                )
                os.makedirs(tile_output_dir, exist_ok=True)
                output_filepath = os.path.join(tile_output_dir, f"{bitrate}.mp4")

                # Take a chunk, crop tile, and encode it at target bitrate
                encode_command = [
                    "ffmpeg",
                    "-i",
                    chunk_path,
                    "-vf",
                    crop_filter,
                    "-c:v",
                    "libx265",
                    "-b:v",
                    bitrate,
                    "-preset",
                    "medium",
                    "-an",
                    output_filepath,
                ]

                # print(f"Running: {' '.join(encode_command)}")
                subprocess.run(encode_command, check=True, capture_output=True)

print(f"Successfully processed {chunk_file} -> tile_{row}_{col} @ {bitrate}")

print("All video assets prepared.")
