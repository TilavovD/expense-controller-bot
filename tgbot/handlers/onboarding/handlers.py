
import datetime
from math import prod

from django.utils import timezone
from telegram import ParseMode, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding import keyboards

from cart.models import Cart

ORDER, CART, PLOV, SALADS, CONTACT_US, FEEDBACK = range(6)

def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=keyboards.make_keyboard_for_start_command())
    return ConversationHandler.END

def order(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Buyurtma qilish uchun quyidagilardan birini tanlang",
                              reply_markup=keyboards.make_keyboard_for_order())
    return ORDER
    
def cart(update: Update, context: CallbackContext) -> None:
    cart_products = Cart.objects.all()
    text = "Sizning savatchangiz bo'sh"
    
    if cart_products:
        
        print("if ni ichiga kiryapti")
        print(f"cart_products----{cart_products}")
        text = "Sizning savatchangizda: \n"
        reply_markup, text, sum = keyboards.make_keyboard_for_cart(cart_products, text)            
        text += f"\n\n Umumiy summa: {sum}"
    
    
    
    update.message.reply_text(text=text, reply_markup=reply_markup)
    return ORDER


def contact_us(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Agar sizda savollar bo'lsa bizga telefon qilishingiz mumkin: +99898 368 7875",
                              reply_markup=keyboards.make_keyboard_for_start_command())
    return ConversationHandler.END

def feedback(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="SamOshni tanlaganingiz uchun rahmat.",
                              reply_markup=keyboards.make_keyboard_for_feedback())
    return FEEDBACK

def back_to_main(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Davom etamizmi?",
                              reply_markup=keyboards.make_keyboard_for_start_command())
    return ConversationHandler.END

def order_plov(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Oshni tanlash menyusi",
                              reply_markup=keyboards.make_keyboard_for_plov())
    return PLOV

def order_salad(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Oshni tanlash menyusi",
                              reply_markup=keyboards.make_keyboard_for_salad())
    return SALADS









def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )