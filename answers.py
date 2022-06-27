import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


def env(key):
    return os.getenv(key)


class Answers(Enum):
    HELP = "У разі необхідності термінової консультації звертайтесь за телефонами:\n" + \
           f"<code>{env('HELP1_NUM')}</code> (<b>{env('HELP1_NAME')}</b>)\n" + \
           f"<code>{env('HELP2_NUM')}</code> (<b>{env('HELP2_NAME')}</b>)"
    NO_ATTACHMENTS = "Ви повинні додати <b>відео файл(и)</b> з підписом(<b>виконавець</b>, <b>автор</b>, <b>назва твору</b>)."
    NO_CAPTION = "Кожен відофайл повинен бути підписаний: <b>Прізвище</b>, <b>ім'я</b>, <b>по батькові</b>"
    SCHEDULE = f"<b>{env('CONSULT_START')}</b> та <b>{env('CONSULT_END')}</b> - Відбудуться <b>констультації на платформі " + \
               f"Zoom</b>(id: <code>{env('ZOOM_ID')}</code>; password: <code>{env('ZOOM_PASS')}</code>)\n\n" + \
               "Для складання іспиту \"Творчий конкурс\" вам потрібно надіслати боту запис виконання:\n" + \
               f"<b>{env('POEM')}</b> - <b>Літературних творів</b>(уривок з прози, вірш, байка, монолог)\n" + \
               f"<b>{env('VOCAL')}</b> - <b>Вокальних творів</b>\n" + \
               f"<b>{env('CHOREOGRAPHY')}</b> - <b>Хореографічних композицій</b>\n" + \
               f"<b>{env('ETUDES')}</b> - <b>Етюдів</b>\nЗгідно з програмою творчого конкурсу\n\n" + \
               f"<b>{env('LETTER')}</b> - <b>Мотиваційний лист</b>"
    START = f"Переконайтесь, будь ласка, що Ви створили <a href='{env('ADMISSION_LINK')}'>електронний кабінет</a> " + \
            f"та подали <a href='{env('APPLICATION_LINK')}'>заявку</a> на творчий конкурс.\n\n" + \
            "Також хочемо повідомити, що бот має корисне меню в лівому нижньому кутку."
    SUBMITTED = "Дякуємо, ми отримали Ваші файл(и)."
    NO_INTEREST = "Ви повинні додати <b>відео файл(и)</b> з підписом(<b>виконавець</b>, <b>автор</b>, <b>назва твору</b>)."
