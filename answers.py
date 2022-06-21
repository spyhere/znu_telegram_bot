import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


def env(key):
    return os.getenv(key)


class Answers(Enum):
    APPLY = f"<a href='{env('APPLICATION_LINK')}'>Подати заявку</a>"
    HELP = "У разі необхідності термінової консультації звертайтесь за телефонами:\n" + \
           f"<code>{env('HELP1_NUM')}</code> (<b>{env('HELP1_NAME')}</b>)\n" + \
           f"<code>{env('HELP2_NUM')}</code> (<b>{env('HELP2_NAME')}</b>)"
    LETTER_INSTRUCTIONS = "Надішліть боту текстовий файл із мотиваційним листом. Будь ласка, назвіть файл у форматі: " + \
                          "<b>Прізвище, ім'я, по батькові – Мотиваційний лист</b>.\n\n" + \
                          "Формати, які ми підтримуємо: " + \
                          "<code>pdf</code>, <code>txt</code>, <code>doc</code>, <code>docm</code>, <code>docx</code>, " + \
                          "<code>dot</code>, <code>dotm</code>, <code>dotx</code>, <code>odt</code>, <code>rtf</code>"
    LETTER_SUBMITTED = "Дякуємо, ми отримали Ваш мотиваційний лист!"
    NO_ATTACHMENTS = "Ви повинні додати <b>відео файл(и)</b> з підписом(<b>виконавець</b>, <b>автор</b>, <b>назва твору</b>)."
    NO_CAPTION = "Кожен відофайл повинен бути підписаний: <b>Прізвище</b>, <b>ім'я</b>, <b>по батькові</b>"
    START = f"<b>{env('CONSULT_START')}</b> та <b>{env('CONSULT_END')}</b> - Відбудуться <b>констультації на платформі " + \
            f"Zoom</b>(id: <code>{env('ZOOM_ID')}</code>; password: <code>{env('ZOOM_PASS')}</code>)\n\n" + \
            "Для складання іспиту \"Творчий конкурс\" вам потрібно надіслати запис виконання:\n" + \
            f"<b>{env('POEM')}</b> - <b>Літературних творів</b>(уривок з прози, вірш, байка, монолог)\n" + \
            f"<b>{env('VOCAL')}</b> - <b>Вокальних творів</b>\n" + \
            f"<b>{env('CHOREOGRAPHY')}</b> - <b>Хореографічних композицій</b>\n" + \
            f"<b>{env('ETUDES')}</b> - <b>Етюдів\nЗгідно з програмою творчого конкурсу</b>\n\n" + \
            f"<b>{env('LETTER')}</b> - <b>Мотиваційний лист</b>"
    SUBMITTED = "Дякуємо, ми отримали Ваші файл(и)."
    NO_INTEREST = "Ви повинні додати <b>відео файл(и)</b> з підписом(<b>виконавець</b>, <b>автор</b>, <b>назва твору</b>)."
    WRONG_MIME_TYPE = "<b>Неправильний формат файлу!</b>\nМи підтримуємо такі формати: " + \
                      "<code>pdf</code>, <code>txt</code>, <code>doc</code>, <code>docm</code>, <code>docx</code>, " + \
                      "<code>dot</code>, <code>dotm</code>, <code>dotx</code>, <code>odt</code>, <code>rtf</code>"
