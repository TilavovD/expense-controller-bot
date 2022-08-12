from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

DEPOZIT = "Depozit"
XARAJAT = "Xarajat"
XISOBOT = "Xisobot"
BACK = "⬅️Ortga"


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    buttons = [
        [DEPOZIT, XARAJAT],
        [XISOBOT],
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_xisobot_command() -> ReplyKeyboardMarkup:
    buttons = [
        ["Depozitlar", "Xarajatlar"],
        [BACK]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_xisobot_command2() -> ReplyKeyboardMarkup:
    buttons = [
        ["Bugungi", "Umumiy"],
        [BACK]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
