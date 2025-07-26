import os
from bot import data, download_dir
from pyrogram.types import Message
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height

def on_task_complete():
    del data[0]
    if len(data) > 0:
        add_task(data[0])

def add_task(message: Message):
    try:
        msg = message.reply_text("📥 Downloading video...", quote=True)
        filepath = message.download(file_name=download_dir)
        msg.edit("🎞 Encoding video...")
        new_file = encode(filepath)
        if new_file:
            msg.edit("📊 Getting metadata...")
            duration = get_duration(new_file)
            thumb = get_thumbnail(new_file, download_dir, duration / 4)
            width, height = get_width_height(new_file)
            msg.edit("📤 Uploading video...")
            message.reply_video(
                new_file,
                quote=True,
                supports_streaming=True,
                thumb=thumb,
                duration=duration,
                width=width,
                height=height
            )
            os.remove(new_file)
            os.remove(thumb)
            try:
                msg.edit("✅ Video Encoded to x265")
            except MessageNotModified:
                pass
        else:
            msg.edit("❌ Encoding failed. Maybe already HEVC format.")
            os.remove(filepath)
    except Exception as e:
        try:
            msg.edit(f"<code>{e}</code>", parse_mode="HTML")
        except MessageNotModified:
            pass
    on_task_complete()
