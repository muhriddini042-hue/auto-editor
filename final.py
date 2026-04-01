import subprocess

def add_audio(video, audio):
    output = video.replace(".mp4", "_final.mp4")

    cmd = [
        "ffmpeg",
        "-i", video,
        "-i", audio,
        "-shortest",
        "-y",
        output
    ]

    subprocess.run(cmd)
    return output
