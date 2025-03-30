import os
import cv2
import numpy as np
from pydub import AudioSegment
import subprocess


def create_travel_video(image_paths, output_path, effect="fade", music="adventure"):
    """Generates a travel video from images with effects and music."""
    frame_list = []
    
    # Load and resize images
    for image_path in image_paths:
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Error: Could not read image {image_path}")
            continue
        img = cv2.resize(img, (1280, 720))
        frame_list.append(img)

    if not frame_list:
        print("❌ Error: No valid images provided.")
        return

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, 30, (1280, 720))

    # Apply effects
    if effect == "fade":
        for i in range(len(frame_list) - 1):
            for alpha in np.linspace(0, 1, 30):
                frame = cv2.addWeighted(frame_list[i], 1 - alpha, frame_list[i + 1], alpha, 0)
                video_writer.write(frame)

    elif effect == "slide":
        for i in range(len(frame_list) - 1):
            for offset in np.linspace(0, 1280, 30):
                frame = np.zeros_like(frame_list[i])
                offset = int(offset)
                frame[:, offset:, :] = frame_list[i][:, :1280 - offset, :]
                frame[:, :offset, :] = frame_list[i + 1][:, 1280 - offset:, :]
                video_writer.write(frame)

    elif effect == "zoom":
        for img in frame_list:
            h, w, _ = img.shape
            for scale in np.linspace(1, 1.5, 30):
                zoomed = cv2.resize(img, None, fx=scale, fy=scale)
                zoomed_h, zoomed_w, _ = zoomed.shape

                # Center-crop the zoomed frame
                start_h = (zoomed_h - h) // 2
                start_w = (zoomed_w - w) // 2
                cropped = zoomed[start_h:start_h + h, start_w:start_w + w]
                video_writer.write(cropped)

    # Write frames to video
    for frame in frame_list:
        video_writer.write(frame)

    video_writer.release()

    # Add background music using pydub
    music_path = f"media/music/{music}.mp3"
    if os.path.exists(music_path):
        try:
            # Load audio
            audio = AudioSegment.from_file(music_path)
            video_duration = len(frame_list) / 30  # Assuming 30 FPS
            audio_duration = len(audio) / 1000  # Convert to seconds

            # Loop audio to match video duration
            if audio_duration < video_duration:
                loops_needed = int(video_duration // audio_duration) + 1
                audio = audio * loops_needed  # Repeat the audio

            # Save audio to a temporary file
            temp_audio_path = "temp_audio.mp3"
            audio.export(temp_audio_path, format="mp3")

            # Merge audio and video using ffmpeg
            final_output_path = output_path.replace(".mp4", "_with_audio.mp4")
            ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

            # Use subprocess for better error handling
            command = [
                ffmpeg_path,
                "-y",
                "-i", output_path,
                "-i", temp_audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",  # Ensure audio and video are the same length
                "-map", "0:v:0",  # Use video from first input
                "-map", "1:a:0",  # Use audio from second input
                final_output_path
            ]
            
            # Execute the FFmpeg command
            subprocess.run(command, check=True, capture_output=True)

            # Remove temporary files
            os.remove(temp_audio_path)
            os.remove(output_path)  # Remove the video without audio

            print(f"✅ Video with audio saved at {final_output_path}")
            return final_output_path  # Return the path of the video with audio
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error adding music: {e}")
            return output_path
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return output_path
    else:
        print(f"⚠️ Music file not found: {music_path}")
        return output_path