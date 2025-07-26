import os
import time
import ffmpeg
from subprocess import call, check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


def get_codec(filepath, channel='v:0'):
    try:
        output = check_output([
            'ffprobe', '-v', 'error', '-select_streams', channel,
            '-show_entries', 'stream=codec_name', '-of',
            'default=nokey=1:noprint_wrappers=1', filepath
        ])
        return output.decode('utf-8').strip().split()
    except Exception:
        return []


def encode(filepath):
    basefilepath, extension = os.path.splitext(filepath)
    output_filepath = basefilepath + '_480p_HEVC.mp4'

    if os.path.isfile(output_filepath):
        print(f'Skipping "{filepath}": output already exists')
        return output_filepath

    print(f'Encoding {filepath} to 480p HEVC...')

    # Re-encode with 480p scale and H.265 compression
    cmd = [
        "ffmpeg", "-i", filepath,
        "-vf", "scale=-2:480",
        "-c:v", "libx265",
        "-preset", "fast",
        "-crf", "28",
        "-c:a", "aac",
        "-b:a", "128k",
        output_filepath
    ]

    call(cmd)

    # Optional: delete the original file
    os.remove(filepath)

    return output_filepath


def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
            .input(in_filename, ss=ttl)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error:
        return None


def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata and metadata.has("duration"):
        return metadata.get('duration').seconds
    return 0


def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata and metadata.has("width") and metadata.has("height"):
        return metadata.get("width"), metadata.get("height")
    return 1280, 720  # default fallback
