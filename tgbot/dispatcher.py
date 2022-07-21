import sys
import logging
from typing import Dict

import telegram.error
from telegram import Bot, Update, BotCommand, ReplyKeyboardRemove   
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, CallbackContext, 
)

from dtb.celery import app  # event processing in async mode
from dtb.settings import TELEGRAM_TOKEN, DEBUG

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command
from tgbot.handlers.onboarding.keyboards import DEPOZIT, XARAJAT, XISOBOT, BACK

def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    DEPOSIT_QUESTION, DEPOSIT_PRICE, XARAJAT_QUESTION, XARAJAT_PRICE, XISOBOTLAR, XISOBOT_BUGUN, XISOBOT_UMUMIY = range(7)
    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)
    
    #Conversation_handler_starts
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', onboarding_handlers.command_start),
            MessageHandler(Filters.text(DEPOZIT), onboarding_handlers.depozit_comment_qustion),  
            MessageHandler(Filters.text(XARAJAT), onboarding_handlers.xarajat_comment_qustion),
            MessageHandler(Filters.text(XISOBOT), onboarding_handlers.xisobot_tanlovi),           
            ],
        states={
            DEPOSIT_QUESTION: [
                MessageHandler(Filters.text & ~Filters.text(BACK) & ~Filters.command, onboarding_handlers.depozit_comment),
            ],
            DEPOSIT_PRICE: [
                MessageHandler(Filters.text & ~Filters.text(BACK) & ~Filters.command, onboarding_handlers.depozit_price),

                ],  
            XARAJAT_QUESTION: [
                MessageHandler(Filters.text & ~Filters.text(BACK) & ~Filters.command, onboarding_handlers.xarajat_comment),
            ],
            XARAJAT_PRICE: [
                MessageHandler(Filters.text & ~Filters.text(BACK) & ~Filters.command, onboarding_handlers.xarajat_price),

                ],
            XISOBOTLAR: [
                MessageHandler(Filters.text("Bugungi"), onboarding_handlers.xisobot_bugun),  
                MessageHandler(Filters.text("Umumiy"), onboarding_handlers.xisobot_umumiy),
                MessageHandler(Filters.text(BACK), onboarding_handlers.asosiy_sahifaga_qaytish),
                 ],  
            XISOBOT_BUGUN: [
                MessageHandler(Filters.text("Depozitlar"), onboarding_handlers.depozit_xisobot_bugun),  
                MessageHandler(Filters.text("Xarajatlar"), onboarding_handlers.xarajat_xisobot_bugun),
                MessageHandler(Filters.text(BACK), onboarding_handlers.asosiy_sahifaga_qaytish),
                 ],  
            XISOBOT_UMUMIY: [
                MessageHandler(Filters.text("Depozitlar"), onboarding_handlers.depozit_xisobot_all),  
                MessageHandler(Filters.text("Xarajatlar"), onboarding_handlers.xarajat_xisobot_all),
                MessageHandler(Filters.text(BACK), onboarding_handlers.asosiy_sahifaga_qaytish),
                 ], 
                                   
           
        },
        fallbacks=[],
        allow_reentry =  True
    )

    dp.add_handler(conv_handler)
    
    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


# Global variable - best way I found to init Telegram bot
bot = Bot(TELEGRAM_TOKEN)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def set_up_commands(bot_instance: Bot) -> None:
    langs_with_commands: Dict[str, Dict[str, str]] = {
        'en': {
            'start': 'Start django bot 🚀',
            'stats': 'Statistics of bot 📊',
            'admin': 'Show admin info ℹ️',
            'ask_location': 'Send location 📍',
            'broadcast': 'Broadcast message 📨',
            'export_users': 'Export users.csv 👥',
        },
        'es': {
            'start': 'Iniciar el bot de django 🚀',
            'stats': 'Estadísticas de bot 📊',
            'admin': 'Mostrar información de administrador ℹ️',
            'ask_location': 'Enviar ubicación 📍',
            'broadcast': 'Mensaje de difusión 📨',
            'export_users': 'Exportar users.csv 👥',
        },
        'fr': {
            'start': 'Démarrer le bot Django 🚀',
            'stats': 'Statistiques du bot 📊',
            'admin': "Afficher les informations d'administrateur ℹ️",
            'ask_location': 'Envoyer emplacement 📍',
            'broadcast': 'Message de diffusion 📨',
            "export_users": 'Exporter users.csv 👥',
        },
        'ru': {
            'start': 'Запустить django бота 🚀',
            'stats': 'Статистика бота 📊',
            'admin': 'Показать информацию для админов ℹ️',
            'broadcast': 'Отправить сообщение 📨',
            'ask_location': 'Отправить локацию 📍',
            'export_users': 'Экспорт users.csv 👥',
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
            ]
        )


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
set_up_commands(bot)

n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
