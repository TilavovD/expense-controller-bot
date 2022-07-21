
import datetime
from math import prod

from django.utils import timezone
from telegram import ParseMode, ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding import keyboards

from depozit.models import Depozit
from xarajat.models import Xarajat

DEPOSIT_QUESTION, DEPOSIT_PRICE, XARAJAT_QUESTION, XARAJAT_PRICE, XISOBOTLAR, XISOBOT_BUGUN, XISOBOT_UMUMIY = range(7)
def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=keyboards.make_keyboard_for_start_command())
    return ConversationHandler.END

def depozit_comment_qustion(update:Update, context: CallbackContext):
    update.message.reply_text(text="Depozit manbasini kiriting: ")
    return DEPOSIT_QUESTION

def xarajat_comment_qustion(update:Update, context: CallbackContext):
    update.message.reply_text(text="Qayerga ishlatganingiz haqida izoh kiriting: ")
    return XARAJAT_QUESTION
    
def depozit_comment(update:Update, context: CallbackContext):
    manba = update.message.text
    Depozit.objects.create(comment=manba, user_id=update.message.chat_id)
    update.message.reply_text(text="Summani kiriting (UZS): ")
    
    print(manba)
    return DEPOSIT_PRICE

def xarajat_comment(update:Update, context: CallbackContext):
    izoh = update.message.text
    Xarajat.objects.create(comment=izoh, user_id=update.message.chat_id)
    update.message.reply_text(text="Summani kiriting (UZS): ")
    
    print(izoh)
    return XARAJAT_PRICE
    
def depozit_price(update:Update, context: CallbackContext):
    price = update.message.text
    try:
        price=int(price)
    except:
        update.message.reply_text("Price must be integer")
        update.message.reply_text(text="Summani kiriting (UZS): ")
        return DEPOSIT_PRICE
    depozit = Depozit.objects.latest("created_at")
    depozit.price = price
    depozit.save()
    update.message.reply_text(text="Depozit saqlandi. Davom etamizmi?!", reply_markup=keyboards.make_keyboard_for_start_command())


def xarajat_price(update:Update, context: CallbackContext):
    price = update.message.text
    try:
        price=int(price)
    except:
        update.message.reply_text("Summa butun son bo'lishi kerak")
        update.message.reply_text(text="Summani kiriting (UZS): ")
        return XARAJAT_PRICE

    xarajat = Xarajat.objects.latest("created_at")
    xarajat.price = price
    xarajat.save()
    update.message.reply_text(text="Xarajat saqlandi. Davom etamizmi?!", reply_markup=keyboards.make_keyboard_for_start_command())

def xisobot_bugun(update:Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:",
        reply_markup=keyboards.make_keyboard_for_xisobot_command())
    return XISOBOT_BUGUN

def xisobot_umumiy(update:Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:",
        reply_markup=keyboards.make_keyboard_for_xisobot_command())
    return XISOBOT_UMUMIY

def depozit_xisobot_all(update:Update, context: CallbackContext):
    deposits = Depozit.objects.all()
    price = 0
    text = "Umumiy depozitlar: \n\n"
    for deposit in deposits:
        text+=f"{str(deposit.comment).capitalize()} - {deposit.price} so'm\n"
        price+=deposit.price
    text+=f"\n\nUmumiy summa: {price} so'm"
    update.message.reply_text(text)
def xarajat_xisobot_all(update:Update, context: CallbackContext):
    xarajatlar = Xarajat.objects.all()
    price = 0
    text = "Umumiy xarajatlar: \n\n"
    for xarajat in xarajatlar:
        text+=f"{str(xarajat.comment).capitalize()} - {xarajat.price} so'm\n"
        price+=xarajat.price
    text+=f"\n\nUmumiy summa: {price} so'm"
    update.message.reply_text(text)

def depozit_xisobot_bugun(update:Update, context: CallbackContext):
    depozits = Depozit.objects.filter(date=datetime.date.today()).all()
    price = 0
    text = "Bugungi depozitlar: \n\n"
    for depozit in depozits:
        text+=f"{str(depozit.comment).capitalize()} - {depozit.price} so'm |{depozit.created_at.time().strftime('%H:%M')}\n"
        price+=depozit.price

        
    text+=f"\n\nUmumiy summa: {price} so'm"
    update.message.reply_text(text)
def xarajat_xisobot_bugun(update:Update, context: CallbackContext):
    xarajatlar = Xarajat.objects.filter(date=datetime.date.today()).all()
    price = 0
    text = "Bugungi xarajatlar: \n\n"
    for xarajat in xarajatlar:
        text+=f"{str(xarajat.comment).capitalize()} - {xarajat.price} so'm | {xarajat.created_at.time().hour}:{xarajat.created_at.time().minute}\n"
        price+=xarajat.price

        
    text+=f"\n\nUmumiy summa: {price} so'm"
    update.message.reply_text(text)

def asosiy_sahifaga_qaytish(update:Update, context: CallbackContext):
    update.message.reply_text(text="Hisob-kitob ishlarini davom ettiramizmi?", reply_markup=keyboards.make_keyboard_for_start_command())

def xisobot_tanlovi(update:Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:", reply_markup=keyboards.make_keyboard_for_xisobot_command2())
    return XISOBOTLAR

def xisobot_tanlovi_bugun(update:Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:", reply_markup=keyboards.make_keyboard_for_xisobot_command())

def xisobot_tanlovi_umumiy(update:Update, context: CallbackContext):
    update.message.reply_text(text="Bo'limni tanlang:", reply_markup=keyboards.make_keyboard_for_xisobot_command())


    




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