import subprocess
import os
from pathlib import Path

def convert_to_h264(file_path):
    tmp_path = file_path.with_name(file_path.stem + "_tmp.mp4")
    print(f"Converting: {file_path} -> {tmp_path}")

    # Run ffmpeg to convert to H.264
    cmd = [
        "ffmpeg", "-y",
        "-i", str(file_path),
        "-vcodec", "libx264",
        "-profile:v", "baseline",
        "-level", "3.0",
        "-acodec", "aac",
        str(tmp_path)
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if tmp_path.exists():
        tmp_path.replace(file_path)
        print(f"✅ Replaced original with converted: {file_path}")
    else:
        print(f"❌ Failed to convert: {file_path}")
        print(result.stderr.decode())

def main(root_dir="."):
    root = Path(root_dir)
    for mp4_file in root.rglob("*.mp4"):
        if "_tmp" in mp4_file.stem:
            continue  # Skip temp files
        convert_to_h264(mp4_file)

if __name__ == "__main__":
    import sys
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    main(directory)

