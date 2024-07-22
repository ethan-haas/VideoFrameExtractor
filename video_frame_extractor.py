import os
import av
import shutil
import logging
import argparse
import glob
from multiprocessing import Pool, cpu_count
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_frames_from_video(video_path, frame_numbers, frame_folder, image_format, quality):
    try:
        with av.open(video_path) as container:
            stream = container.streams.video[0]
            stream.codec_context.skip_frame = 'NONKEY'
            frame_gen = (frame for frame in container.decode(stream))

            for frame_number in frame_numbers:
                target_pts = int(frame_number / stream.average_rate * stream.time_base.denominator)

                # Find the correct frame
                frame_found = False
                for frame in frame_gen:
                    if frame.pts >= target_pts:
                        pil_image = frame.to_image()
                        frame_path = os.path.join(frame_folder, f"frame_{frame_number:04d}.{image_format}")

                        if image_format.lower() == "jpg":
                            pil_image.save(frame_path, quality=quality)
                        elif image_format.lower() == "png":
                            pil_image.save(frame_path, compress_level=0)
                        else:
                            pil_image.save(frame_path)
                        
                        frame_found = True
                        break

                if not frame_found:
                    logging.warning(f"Frame {frame_number} with target_pts {target_pts} not found in {video_path}")

    except Exception as e:
        logging.error(f"Error processing {video_path} with frames {frame_numbers}: {e}", exc_info=True)

def extract_frames(video_path, output_folder, include_parent=False, image_format="jpg", frame_skip=1, quality=100, num_processes=cpu_count()):
    os.makedirs(output_folder, exist_ok=True)
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    if include_parent:
        parent_folder = os.path.dirname(video_path)
        frame_folder = os.path.join(output_folder, os.path.basename(parent_folder), video_name)
    else:
        frame_folder = os.path.join(output_folder, video_name)

    if os.path.exists(frame_folder):
        shutil.rmtree(frame_folder)
    os.makedirs(frame_folder)

    try:
        with av.open(video_path) as container:
            stream = container.streams.video[0]
            fps = stream.average_rate
            frame_count = stream.frames
            format_name = container.format.name
            video_size = (stream.codec_context.width, stream.codec_context.height)
    except Exception as e:
        logging.error(f"Error opening video {video_path}: {e}", exc_info=True)
        return

    logging.info(f"Video Details:")
    logging.info(f"  Format: {format_name}")
    logging.info(f"  Size: {video_size[0]}x{video_size[1]}")
    logging.info(f"  FPS: {fps}")
    logging.info(f"  Frame Count: {frame_count}")

    frame_numbers = range(0, frame_count, frame_skip)
    total_frames_to_extract = len(frame_numbers)
    frame_chunks = [frame_numbers[i:i + (total_frames_to_extract // num_processes) + 1] for i in range(0, total_frames_to_extract, (total_frames_to_extract // num_processes) + 1)]

    logging.info("Starting frame extraction...")
    try:
        with Pool(processes=num_processes) as pool:
            pool.starmap(extract_frames_from_video, [(video_path, chunk, frame_folder, image_format, quality) for chunk in frame_chunks])
        logging.info("Frame extraction completed.")
    except Exception as e:
        logging.error(f"Error during frame extraction: {e}", exc_info=True)

def main():
    parser = argparse.ArgumentParser(description="Extract frames from video file(s)")
    parser.add_argument("-i", "--input", required=True, help="Path to the input video file or directory")
    parser.add_argument("-o", "--output", default="", help="Path to the output directory")
    parser.add_argument("-p", "--parent", action="store_true", help="Include the parent directory of the video in the output directory path")
    parser.add_argument("-f", "--format", default="jpg", choices=["jpg", "png"], help="Image format for extracted frames (default: jpg)")
    parser.add_argument("--frame_skip", type=int, default=1, help="Number of frames to skip between extractions (default: 1)")
    parser.add_argument("--quality", type=int, default=100, help="Quality of the extracted images (default: 100 for JPG)")
    parser.add_argument("--processes", type=int, default=cpu_count(), help="Number of processes to use (default: number of CPU cores)")
    args = parser.parse_args()

    if args.output == "":
        args.output = os.path.dirname(args.input)

    if os.path.isfile(args.input):
        extract_frames(args.input, args.output, args.parent, args.format, args.frame_skip, args.quality, args.processes)
    elif os.path.isdir(args.input):
        video_files = glob.glob(os.path.join(args.input, "*.mp4")) + \
                      glob.glob(os.path.join(args.input, "*.mkv")) + \
                      glob.glob(os.path.join(args.input, "*.avi")) + \
                      glob.glob(os.path.join(args.input, "*.mov"))
        if not video_files:
            logging.warning("No video files found in the input directory.")
        else:
            for video_file in video_files:
                extract_frames(video_file, args.output, args.parent, args.format, args.frame_skip, args.quality, args.processes)
    else:
        logging.error("Invalid input: not a file or directory")

if __name__ == "__main__":
    main()
