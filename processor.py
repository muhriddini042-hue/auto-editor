import librosa
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def create_rhythm_video(image_paths, audio_path, output_path):
    # 1. Musiqa bitlarini aniqlash
    y, sr = librosa.load(audio_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # 2. Videokliplarni yaratish
    clips = []
    num_images = len(image_paths)
    
    for i in range(len(beat_times) - 1):
        if i >= num_images: # Rasmlar tugab qolsa, qaytadan aylantiradi
            img_path = image_paths[i % num_images]
        else:
            img_path = image_paths[i]
            
        start_t = beat_times[i]
        end_t = beat_times[i+1]
        duration = end_t - start_t
        
        # Har bir rasmni bit davomiyligicha ko'rsatish
        img_clip = ImageClip(img_path).set_duration(duration).set_fps(24)
        
        # Oddiy effekt: Kattalashish (Zoom) - ixtiyoriy
        img_clip = img_clip.resize(lambda t: 1 + 0.05 * t) 
        
        clips.append(img_clip)

    # 3. Kliplarni birlashtirish va musiqa qo'shish
    final_clip = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(audio_path)
    final_clip = final_clip.set_audio(audio)
    
    # 4. Saqlash
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
