#!/usr/bin/env python3
import os
import cv2
import glob
from pathlib import Path

from cv2.gapi import video


def extract_frames(video_path, output_dir):
    """
    Extract the first and last frames from a video and save them as thumbnails.

    Args:
        video_path: Path to the video file
        output_dir: Directory to save the thumbnails
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get video filename without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Get total frame count
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        print(f"Error: Video {video_path} has no frames")
        cap.release()
        return

    # Extract first frame
    ret, first_frame = cap.read()
    if ret:
        first_frame_path = os.path.join(output_dir, f"{video_name}_thumb_first.png")
        cv2.imwrite(first_frame_path, first_frame)
        print(f"Saved first frame: {first_frame_path}")
    else:
        print(f"Error: Could not read first frame from {video_path}")

    # For last frame, try a more robust approach
    # Some videos might have issues with direct seeking to the last frame
    # Reset the video capture and read frames sequentially if needed
    cap.release()
    cap = cv2.VideoCapture(video_path)

    # Try to get the last frame by seeking directly first
    cap.set(
        cv2.CAP_PROP_POS_FRAMES, max(0, total_frames - 2)
    )  # Try second-to-last frame to be safe
    ret, last_frame = cap.read()

    # If direct seeking failed, try reading all frames
    if not ret:
        print(
            f"Direct seeking to last frame failed for {video_path}, trying sequential read..."
        )
        cap.release()
        cap = cv2.VideoCapture(video_path)
        last_frame = None
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            last_frame = frame

    # Save the last frame if we got one
    if last_frame is not None:
        last_frame_path = os.path.join(output_dir, f"{video_name}_thumb_last.png")
        cv2.imwrite(last_frame_path, last_frame)
        print(f"Saved last frame: {last_frame_path}")
    else:
        print(f"Error: Could not read last frame from {video_path}")

    # Release the video capture object
    cap.release()


def main():
    # Define paths
    script_dir = Path(__file__).parent
    video_dir = script_dir / "medias"
    output_dir = video_dir

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get all video files
    video_files = glob.glob(str(video_dir / "*.mp4"))

    if not video_files:
        print(f"No video files found in {video_dir}")
        return

    print(f"Found {len(video_files)} video files")

    # Process each video
    for video_path in video_files:
        print(f"Processing {video_path}...")
        extract_frames(video_path, output_dir)

    print("Thumbnail extraction complete!")


if __name__ == "__main__":
    main()

