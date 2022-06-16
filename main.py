import asyncio
import logging
from answers import Answers

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message

API_TOKEN = '5581388532:AAH7nk3mp5QBCwwXz2zubxXNfcDqH9rxROM'
CHANNEL_ID = '-1001630316640'

# Initialize bot and dispatcher
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.answer(Answers.START.value)


@dp.message_handler(commands=['help'])
async def send_help(message: Message):
    await message.answer(Answers.HELP.value)


media = {}
break_handler = {}


@dp.message_handler(
    content_types=[ContentType.VIDEO, ContentType.PHOTO, ContentType.TEXT])
async def message_handler(message: Message):
    global break_handler
    global media

    user_id = message.from_user.id
    if user_id in break_handler:
        return

    if message.content_type == "text":
        await message.answer(Answers.NO_ATTACHMENTS.value)
        return

    no_caption_single_file = message.caption is None and message.media_group_id is None
    no_caption_media_group = message.caption is None and not media.get(user_id)
    if no_caption_single_file or no_caption_media_group:
        break_handler[user_id] = None
        await message.answer(Answers.NO_CAPTION.value)
        del break_handler[user_id]
        return

    caption = f"@{message.from_user.username}\n\n{message.caption}" if message.caption else None

    if message.media_group_id:
        if not media.get(user_id):
            media[user_id] = types.MediaGroup()

        match message.content_type:
            case 'photo':
                media[user_id].attach_photo(message.photo[-1].file_id, caption)
            case 'video':
                media[user_id].attach_video(message.video.file_id, caption=caption)

        await asyncio.sleep(0.5)
        if media[user_id].media:
            media_group = media[user_id]
            media[user_id] = types.MediaGroup()
            await bot.send_media_group(CHANNEL_ID, media_group)
            await message.answer(Answers.SUBMITTED.value)
            del media[user_id]
            return
    else:
        match message.content_type:
            case 'photo':
                await bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption)
                await message.answer(Answers.SUBMITTED.value)
            case 'video':
                await bot.send_video(CHANNEL_ID, message.video.file_id, caption=caption)
                await message.answer(Answers.SUBMITTED.value)


@dp.message_handler(content_types=[ContentType.ANY])
async def useless_message_handler(message: Message):
    await message.answer(Answers.NO_INTEREST.value)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
