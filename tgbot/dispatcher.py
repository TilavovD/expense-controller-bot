import sys
import logging

import telegram.error
from telegram import Bot
from telegram.ext import (
    Updater, Filters,
    CommandHandler, MessageHandler, ConversationHandler, Dispatcher, CallbackQueryHandler
)

from core.settings import TELEGRAM_TOKEN

from tgbot.handlers.utils import error

from tgbot.handlers.onboarding import handlers as onboarding_handlers

from tgbot.handlers.onboarding.keyboards import DEPOZIT, XARAJAT, XISOBOT, BACK


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    DEPOSIT_QUESTION, DEPOSIT_PRICE, EXPENSE_QUESTION, EXPENSE_PRICE, REPORT, REPORT_TODAY, REPORT_TOTAL, DEPOSIT_DETAIL, \
    DEPOSIT_DELETE_EDIT, DEPOSIT_EDIT, EXPENSE_DETAIL, EXPENSE_DELETE_EDIT, EXPENSE_EDIT = range(13)
    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # Conversation_handler_starts
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', onboarding_handlers.command_start),
            MessageHandler(Filters.text(DEPOZIT), onboarding_handlers.deposit_comment_question),
            MessageHandler(Filters.text(XARAJAT), onboarding_handlers.expense_comment_question),
            MessageHandler(Filters.text(XISOBOT), onboarding_handlers.report_choice),
        ],
        states={
            DEPOSIT_QUESTION: [
                MessageHandler(Filters.text & ~Filters.text(BACK) & ~Filters.command,
                               onboarding_handlers.deposit_comment),
            ],
            DEPOSIT_PRICE: [
                MessageHandler(Filters.text & ~Filters.text(BACK) & ~Filters.command,
                               onboarding_handlers.deposit_price),

            ],
            EXPENSE_QUESTION: [
                MessageHandler(Filters.text & ~Filters.text(BACK) & ~Filters.command,
                               onboarding_handlers.expense_comment),
            ],
            EXPENSE_PRICE: [
                MessageHandler(Filters.text & ~Filters.text(BACK) & ~Filters.command,
                               onboarding_handlers.expense_price),

            ],
            REPORT: [
                MessageHandler(Filters.text("Bugungi"), onboarding_handlers.report_today),
                MessageHandler(Filters.text("Umumiy"), onboarding_handlers.report_total),
                MessageHandler(Filters.text(BACK), onboarding_handlers.back_to_main),
            ],
            REPORT_TODAY: [
                MessageHandler(Filters.text("Depozitlar"), onboarding_handlers.deposit_report_today),
                MessageHandler(Filters.text("Xarajatlar"), onboarding_handlers.expense_report_today),
                MessageHandler(Filters.text(BACK), onboarding_handlers.back_to_main),
            ],
            REPORT_TOTAL: [
                MessageHandler(Filters.text("Depozitlar"), onboarding_handlers.deposit_report_total),
                MessageHandler(Filters.text("Xarajatlar"), onboarding_handlers.expense_report_total),
                MessageHandler(Filters.text(BACK), onboarding_handlers.back_to_main),
            ],
            DEPOSIT_DETAIL: [
                CallbackQueryHandler(onboarding_handlers.deposit_detail),
            ],
            EXPENSE_DETAIL: [
                CallbackQueryHandler(onboarding_handlers.expense_detail),
            ],
            DEPOSIT_DELETE_EDIT: [
                CallbackQueryHandler(onboarding_handlers.deposit_delete_edit),
            ],
            EXPENSE_DELETE_EDIT: [
                CallbackQueryHandler(onboarding_handlers.expense_delete_edit),
            ],

        },
        fallbacks=[],
        allow_reentry=True
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

    print(f"\nPooling of '{bot_link}' started\n")
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

dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, use_context=True))
