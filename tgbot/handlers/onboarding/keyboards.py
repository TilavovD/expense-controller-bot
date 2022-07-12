from telegram import   ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON


def make_keyboard_for_cart(products, text):
    sum = 0
    buttons = []
    for product in products:
            print(f"product-------->{product.product.title}")
            text += f"\n {product.product.title} \n {product.quantity} x {product.product.price} = {product.get_total_price(product)}"
            sum+=product.get_total_price(product)
            buttons.append([
        InlineKeyboardButton(product.product.title),
    ])
    

    return InlineKeyboardMarkup(buttons), text, sum

def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    buttons = [
        ["☎️ Biz bilan aloqa","🛍 Buyurtma berish"],
        ["✍️ Fikr bildirish"]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def make_keyboard_for_plov() -> ReplyKeyboardMarkup:
    buttons = [
        
        ["⬅️ Ortga"]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def make_keyboard_for_salad() -> ReplyKeyboardMarkup:
    buttons = [
        
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