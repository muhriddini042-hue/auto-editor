import os
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from processor import create_rhythm_video  # Video yaratish funksiyasi

# Bot tokeningizni kiriting
TOKEN = "8730826875:AAGJ-yrPY2tOD5eACZDZ_Gt6RZlYlWPPchw"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchi ma'lumotlarini vaqtincha saqlash uchun lug'at
user_data = {}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Salom! Menga bir nechta rasm yuboring, so'ngra musiqani yuboring. Men ulardan ajoyib video tayyorlab beraman!")

@dp.message(F.photo)
async def handle_photos(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'images': [], 'audio': None}
    
    # Rasmni yuklab olish
    photo = message.photo[-1]
    file_path = f"temp/{user_id}_{len(user_data[user_id]['images'])}.jpg"
    
    os.makedirs("temp", exist_ok=True)
    await bot.download(photo, destination=file_path)
    user_data[user_id]['images'].append(file_path)
    
    await message.answer(f"{len(user_data[user_id]['images'])} ta rasm qabul qilindi. Yana rasm yuboring yoki musiqa tashlang.")

@dp.message(F.audio | F.voice)
async def handle_audio(message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_data or not user_data[user_id]['images']:
        await message.answer("Avval rasmlarni yuboring!")
        return

    # Musiqani yuklab olish
    audio = message.audio or message.voice
    audio_path = f"temp/{user_id_audio}.mp3"
    await bot.download(audio, destination=audio_path)
    
    msg = await message.answer("Video tayyorlanmoqda, iltimos kuting...")
    
    # Video yaratish funksiyasini chaqiramiz
    output_video = f"temp/{user_id_result}.mp4"
    try:
        # processor.py ichidagi funksiya
        create_rhythm_video(user_data[user_id]['images'], audio_path, output_video)
        
        # Videoni yuborish
        video_file = types.FSInputFile(output_video)
        await message.answer_video(video_file, caption="Sizning video tayyor! 🔥")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")
    finally:
        # Ma'lumotlarni tozalash
        if user_id in user_data:
            del user_data[user_id]

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
