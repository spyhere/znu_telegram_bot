import os
from dotenv import load_dotenv
import asyncio
import logging
from answers import Answers

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Initialize bot and dispatcher
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.answer(Answers.START.value, 'HTML')


@dp.message_handler(commands=['help'])
async def send_help(message: Message):
    await message.answer(Answers.HELP.value, 'HTML')


@dp.message_handler(commands=['apply'])
async def apply_handler(message: Message):
    await message.answer(Answers.APPLY.value, 'HTML')


media = {}
break_handler = {}


@dp.message_handler(content_types=[ContentType.VIDEO, ContentType.TEXT])
async def message_handler(message: Message):
    global break_handler
    global media

    user_id = message.from_user.id

    # Messages from media group has no caption - skip
    if user_id in break_handler:
        return

    if message.content_type == "text":
        await message.answer(Answers.NO_ATTACHMENTS.value, 'HTML')
        return

    no_caption_single_file = message.caption is None and message.media_group_id is None
    no_caption_media_group = message.caption is None and not media.get(user_id)
    if no_caption_single_file or no_caption_media_group:
        # Intent to skip whole media group
        break_handler[user_id] = None
        await message.answer(Answers.NO_CAPTION.value, 'HTML')
        del break_handler[user_id]
        return

    caption = f"@{message.from_user.username}\n\n{message.caption}" if message.caption else None

    if message.media_group_id:
        if not media.get(user_id):
            media[user_id] = types.MediaGroup()

        media[user_id].attach_video(message.video.file_id, caption=caption)

        await asyncio.sleep(0.5)
        if media[user_id].media:
            media_group = media[user_id]
            media[user_id] = types.MediaGroup()
            await bot.send_media_group(CHANNEL_ID, media_group)
            await message.answer(Answers.SUBMITTED.value, 'HTML')
            del media[user_id]
            return
    else:
        await bot.send_video(CHANNEL_ID, message.video.file_id, caption=caption)
        await message.answer(Answers.SUBMITTED.value, 'HTML')


allowed_mime_types = ['pdf', 'txt', 'doc', 'docm', 'docx', 'dot', 'dotm', 'dotx', 'odt', 'rtf']


@dp.message_handler(content_types=[ContentType.DOCUMENT])
async def motivation_letter_handler(message: Message):
    [file_name, mime_type] = message.document.file_name.split('.')
    if mime_type not in allowed_mime_types:
        await message.answer(Answers.WRONG_MIME_TYPE.value, 'HTML')
        return

    caption = f"@{message.from_user.username}\n\n{file_name}"
    await bot.send_document(CHANNEL_ID, message.document.file_id, caption=caption)
    await message.answer(Answers.SUBMITTED.value, 'HTML')


@dp.message_handler(content_types=[ContentType.ANY])
async def useless_message_handler(message: Message):
    await message.answer(Answers.NO_INTEREST.value, 'HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
