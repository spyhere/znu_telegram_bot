import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


def env(key):
    return os.getenv(key)


sub_dates = [f"<b>{it}</b>" for it in env('SUBMISSION_DATES').split('; ')]


class Answers(Enum):
    HINT = "Для надсилання вашої роботи боту прикріпіть до повідомлення один або кілька " + \
           "відеофайлів і обов'язково підпишіть у форматі: " + \
           "Автор - Назва твору</b>\n\n" + \
           "Для зручності обробки файлів, будь ласка, надсилайте один вид творчої діяльності " + \
           "в окремому повідомленні.\n" + \
           "<i>Наприклад: Хореографія - 1-е повідомлення, Вокал - 2-е повідомлення тощо.</i>\n\n" + \
           "Нагадаємо, ваша <b>програма складається з:</b> " + \
           "<b>літературних творів</b> (уривок з прози, вірш, байка, монолог), " + \
           "<b>вокальних творів</b>, <b>хореографічних композицій</b> та <b>етюдів</b>."
    HELP = "У разі необхідності термінової консультації звертайтесь за телефонами:\n" + \
           f"<code>{env('HELP1_NUM')}</code> (<b>{env('HELP1_NAME')}</b>)\n" + \
           f"<code>{env('HELP2_NUM')}</code> (<b>{env('HELP2_NAME')}</b>)"
    NAME_CHANGED = "Ваше ім'я збережено, <b>%s</b>!"
    NAME_EDIT = "Введіть ваше ім'я правильно."
    NAME_EXISTS = "Вітаємо, <b>%s</b>!\n\n"
    NAME_INPUT = "Введіть ваше ім'я, щоб бот мав можливість підписувати ваші відеоматеріали."
    NAME_RECEIVED = "Приємно познайомитись, <b>%s</b>\nВикористовуйте меню в нижньому лівому кутку для роботи з ботом."
    NO_ATTACHMENTS = "Ви повинні додати <b>відео файл(и)</b> з підписом(<b>виконавець</b>, <b>автор</b>, <b>назва твору</b>)."
    NO_CAPTION = "Кожен відеофайл повинен бути підписаний: <b>Прізвище</b>, <b>ім'я</b>, <b>по батькові</b>"
    SCHEDULE = f"<b>{env('CONSULT_START')}</b> та <b>{env('CONSULT_END')}</b> - Відбудуться <b>констультації на платформі " + \
               f"Zoom</b>(id: <code>{env('ZOOM_ID')}</code>; password: <code>{env('ZOOM_PASS')}</code>)\n\n" + \
               "Для складання іспиту \"Творчий конкурс\" вам потрібно надіслати боту записи виконання " + \
               f"вашої програми в один із перерахованих днів: {', '.join(sub_dates[0:-1])} або {sub_dates[-1]}.\n\n" + \
               "Дивіться в меню пункт <code>\"Підказка\"</code> для правильного надсилання ваших відеоматеріалів."
    START = f"Переконайтесь, будь ласка, що Ви створили <a href='{env('ADMISSION_LINK')}'>електронний кабінет</a> " + \
            f"та подали <a href='{env('APPLICATION_LINK')}'>заявку</a> на творчий конкурс.\n\n"
    SUBMITTED = "Дякуємо, ми отримали Ваші файл(и)."
    NO_INTEREST = "Ви повинні додати <b>відео файл(и)</b> з підписом(<b>виконавець</b>, <b>автор</b>, <b>назва твору</b>)."
