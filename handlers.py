from aiogram import Router, types, F
import os

router = Router()
user_data = {}

BASE_DIR = "storage"

@router.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    os.makedirs(f"{BASE_DIR}/images", exist_ok=True)

    file = await message.bot.get_file(message.photo[-1].file_id)
    path = f"{BASE_DIR}/images/{user_id}_{file.file_id}.jpg"

    await message.bot.download_file(file.file_path, path)

    user_data.setdefault(user_id, {}).setdefault("images", []).append(path)

    await message.answer("Rasm saqlandi 📸")

@router.message(F.audio)
async def handle_audio(message: types.Message):
    user_id = message.from_user.id
    os.makedirs(f"{BASE_DIR}/audio", exist_ok=True)

    file = await message.bot.get_file(message.audio.file_id)
    path = f"{BASE_DIR}/audio/{user_id}.mp3"

    await message.bot.download_file(file.file_path, path)

    user_data.setdefault(user_id, {})["audio"] = path

    await message.answer("Musiqa saqlandi 🎵")

@router.message(F.text == "/start_video")
async def generate(message: types.Message):
    from video_engine.beat import detect_beats
    from video_engine.slideshow import create_slideshow
    from video_engine.final import add_audio
    from video_engine.ai_selector import select_best
    from video_engine.ai_composer import assign_effects

    user_id = message.from_user.id
    data = user_data.get(user_id)

    if not data or "images" not in data or "audio" not in data:
        return await message.answer("Avval rasm va musiqa yubor ❗")

    images = select_best(data["images"])
    audio = data["audio"]

    beats = detect_beats(audio)

    durations = []
    for i in range(len(images)):
        if i < len(beats)-1:
            durations.append(beats[i+1] - beats[i])
        else:
            durations.append(1)

    video = create_slideshow(images, durations)
    final = add_audio(video, audio)

    await message.answer_video(open(final, "rb"))
