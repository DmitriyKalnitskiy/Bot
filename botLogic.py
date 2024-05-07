import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot import token
from aiogram import executor

dp, bot = token()

class MotivationState(StatesGroup):
    sending = State()

@dp.message_handler(commands=['start'])
async def sendWelcome(message: types.Message, state: FSMContext):
    await message.reply("\nДля того, чтобы, бот отправил мотивационное изображение введите команду /photo ."
                        "\nЧтобы просмотреть возможности бота введи команду /info.")

@dp.message_handler(commands=['photo'])
async def send_motivation(message: types.Message, state: FSMContext):
    current_directory = os.getcwd()
    images_directory = os.path.join(current_directory, 'image')
    image_files = [filename for filename in os.listdir(images_directory)
                   if filename.endswith('.jpg') or filename.endswith('.png')]

    if not image_files:
        await message.reply("В папке с изображениями нет файлов.")
        return

    async with state.proxy() as data:
        data.setdefault('index', 0)
        index = data['index']

        image_path = os.path.join(images_directory, image_files[index])

        with open(image_path, 'rb') as photo:
            await bot.send_photo(message.chat.id, photo)

        index += 1
        if index >= len(image_files):
            index = 0

        data['index'] = index

@dp.message_handler(commands=['info'])
async def sendWelcome(message: types.Message):
    await message.reply("Данный бот создан, для того, чтобы поднять вам мотивацию, "
                        "путем отправки мотивационных картинок.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
