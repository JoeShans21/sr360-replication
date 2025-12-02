import os
import json
import argparse
import yt_dlp

parser = argparse.ArgumentParser()
parser.add_argument(
    "--config_url",
    default="config/youtube_sources.json",
    help="Path to config file (default: config/youtube_sources.json)",
)


# list of youtube links. Please change this
LIST_VIDEOS = [
    "-xNN-bJQ4vI",
    "-9YJppTxIDM",
    "93nxeejhPkU",
    "6TlW1ClEBLY",
    "9XR2CZi3V5k",
    "AX4hWfyHr5g",
]


def download_video(
    url, output_folder="./data/video_traces/source_videos", highest=True, save=True
):
    """Download a YouTube video using yt-dlp

    Args:
        url: YouTube URL
        output_folder: Output directory path. Defaults to './data/video_traces/source_videos'.
        highest: If True, download highest quality. Defaults to True.
        save: If True, actually download the video. Defaults to True.
    """

    if not save:
        print("Nothing to be done...")
        return

    try:
        # Create output folder
        os.makedirs(output_folder, exist_ok=True)

        # Configure yt-dlp options
        ydl_opts = {
            "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
            "format": (
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                if highest
                else "worst"
            ),
            "quiet": False,
            "no_warnings": False,
        }

        # Sanitize filename - replace spaces with underscores
        ydl_opts["outtmpl"] = (
            ydl_opts["outtmpl"].replace("%(title)s", "%(title)s").replace(" ", "_")
        )

        print(f"Downloading from: {url}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"Downloaded: {info.get('title', 'Unknown')}")

    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")


if __name__ == "__main__":

    args = parser.parse_args()

    # load json file with the links
    if not args.config_url:
        print("Error: Please provide a config file using --config_url")
        exit(1)

    if not os.path.exists(args.config_url):
        print(f"Error: Config file '{args.config_url}' not found")
        exit(1)

    try:
        input_file_data = json.load(open(args.config_url))
        # iterate over Youtube links
        base_url = input_file_data["URLS"][0]["base_url"]
        folder_ = input_file_data["URLS"][0]["folder"]
        for url_ in input_file_data["URLS"][0]["urls"]:
            url = base_url + url_
            print(url)
            download_video(url, output_folder=folder_, save=True)
    except Exception as e:
        print(f"Error: {e}")
