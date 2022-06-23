import os
import logging

from typing import List
from dotenv import load_dotenv

from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, Message
from aiogram_media_group import media_group_handler

from answers import Answers

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = f"/webhook/{os.getenv('API_TOKEN')}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001

# Initialize bot and dispatcher
bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.answer(Answers.START.value, 'HTML')


@dp.message_handler(commands=['schedule'])
async def schedule_handler(message: Message):
    await message.answer(Answers.SCHEDULE.value, 'HTML')


@dp.message_handler(commands=['help'])
async def send_help(message: Message):
    await message.answer(Answers.HELP.value, 'HTML')


@dp.message_handler(commands=['letter'])
async def letter_instructions_handler(message: Message):
    await message.answer(Answers.LETTER_INSTRUCTIONS.value, 'HTML')


@dp.message_handler(content_types=[ContentType.VIDEO, ContentType.TEXT])
@media_group_handler(only_album=False)
async def message_handler(messages: List[Message]):
    if messages[0].content_type == "text":
        await messages[0].answer(Answers.NO_ATTACHMENTS.value, 'HTML')
        return

    if messages[0].caption is None:
        await messages[0].answer(Answers.NO_CAPTION.value, 'HTML')
        return

    caption = f"@{messages[0].from_user.username}\n\n{messages[0].caption}"

    if len(messages) > 1:
        media_group = types.MediaGroup()
        for ind, message in enumerate(messages):

            if message.content_type != 'video':
                await message.answer(Answers.NO_INTEREST.value, 'HTML')
                return

            media_group.attach_video(
                message.video.file_id,
                caption=(caption if ind == 0 else message.caption),
                caption_entities=message.caption_entities
            )
        await bot.send_media_group(CHANNEL_ID, media_group)
        await messages[0].answer(Answers.SUBMITTED.value, 'HTML')
    else:
        await bot.send_video(CHANNEL_ID, messages[0].video.file_id, caption=caption)
        await messages[0].answer(Answers.SUBMITTED.value, 'HTML')


allowed_mime_types = ['pdf', 'txt', 'doc', 'docm', 'docx', 'dot', 'dotm', 'dotx', 'odt', 'rtf']


@dp.message_handler(content_types=[ContentType.DOCUMENT])
async def motivation_letter_handler(message: Message):
    [file_name, mime_type] = message.document.file_name.split('.')
    if mime_type not in allowed_mime_types:
        await message.answer(Answers.WRONG_MIME_TYPE.value, 'HTML')
        return

    caption = f"@{message.from_user.username}\n\n{file_name}"
    await bot.send_document(CHANNEL_ID, message.document.file_id, caption=caption)
    await message.answer(Answers.LETTER_SUBMITTED.value, 'HTML')


@dp.message_handler(content_types=[ContentType.ANY])
@media_group_handler(only_album=False)
async def useless_message_handler(messages: List[Message]):
    await messages[0].answer(Answers.NO_INTEREST.value, 'HTML')


async def on_startup(db):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(db):
    logging.warning('Shutting down gracefully...')

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
