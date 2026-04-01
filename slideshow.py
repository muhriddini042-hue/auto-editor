import subprocess
import uuid

def create_slideshow(images, durations):
    output = f"storage/outputs/{uuid.uuid4()}.mp4"

    inputs = []
    for i, img in enumerate(images):
        inputs += ["-loop", "1", "-t", str(durations[i]), "-i", img]

    filter_complex = ""
    for i in range(len(images)):
        filter_complex += f"[{i}:v]scale=1080:1920,zoompan=z='min(zoom+0.002,1.5)':d=125[v{i}];"

    concat = "".join([f"[v{i}]" for i in range(len(images))])
    filter_complex += f"{concat}concat=n={len(images)}:v=1:a=0[outv]"

    cmd = [
        "ffmpeg",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-y",
        output
    ]

    subprocess.run(cmd)
    return output
