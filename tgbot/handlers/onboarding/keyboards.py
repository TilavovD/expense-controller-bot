from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.onboarding.static_text import github_button_text, secret_level_button_text


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    buttons = [
        ["☎️ Biz bilan aloqa","🛍 Buyurtma berish"],
        ["✍️ Fikr bildirish"]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def make_keyboard_for_plov() -> ReplyKeyboardMarkup:
    buttons = [
        ["Samarqand Osh Butun", "Samarqand Osh 0.7"],
        ["⬅️ Ortga"]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def make_keyboard_for_salad() -> ReplyKeyboardMarkup:
    buttons = [
        ["Achchiq-chuchuk", "Chimcha"],
        ["⬅️ Ortga"]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def make_keyboard_for_order() -> ReplyKeyboardMarkup:
    buttons = [
        ["📥 Savatcha"],
        ["Samarqand Osh", "Salatlar"],
        ["Asosiyga qaytish"]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def make_keyboard_for_feedback() -> ReplyKeyboardMarkup:
    buttons = [
        ["Hammasi zo'r"],
        ["Chidasa bo'ladi"],
        ["Asosiyga qaytish"]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def make_keyboard_for_quantity():
    buttons = []
    for i in range(1,10,3):
        buttons.append([i, i+1, i+2])
    buttons.append(["⬅️ Ortga"])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)