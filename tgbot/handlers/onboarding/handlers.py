
import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding import keyboards

ORDER, CART, PLOV, PLOV_DETAIL, SALADS, SALAD_DETAIL,  CONTACT_US, FEEDBACK = range(8)

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
    update.message.reply_text(text="Savatchaga xush kelibsiz",
                              reply_markup=keyboards.make_keyboard_for_order())
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

def plov_details(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Samarqand Osh Butun\n\nNarxi: 37950.00 so'm\n\nMol go'shti , zig'ir yog'i, piyoz, yuqori sifatli lazer, sariq va qizil sabzi, mayiz, 1 dona qalampir, 1 dona bedana tuxum", reply_markup=keyboards.make_keyboard_for_quantity())
    return PLOV_DETAIL

def salad_details(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Salad\n\nNarxi: 37950.00 so'm\n\nMol go'shti , zig'ir yog'i, piyoz, yuqori sifatli lazer, sariq va qizil sabzi, mayiz, 1 dona qalampir, 1 dona bedana tuxum", reply_markup=keyboards.make_keyboard_for_quantity())
    return SALAD_DETAIL





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