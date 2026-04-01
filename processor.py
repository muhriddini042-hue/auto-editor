import librosa
import numpy as np

def get_beat_times(audio_path):
    # Musiqani yuklash
    y, sr = librosa.load(audio_path)
    
    # Tempo va bitlarni aniqlash
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    
    # Kadrlarni soniyalarga o'tkazish
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    return beat_times
