import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding import keyboards


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=keyboards.make_keyboard_for_start_command())

def order(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Savatchaga xush kelibsiz",
                              reply_markup=keyboards.make_keyboard_for_order())
    
def cart(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Savatchaga xush kelibsiz",
                              reply_markup=keyboards.make_keyboard_for_order())

def back_to_main(update: Update, context: CallbackContext) -> None:
    pass

def order_plov(update: Update, context: CallbackContext) -> None:
    pass

def order_salad(update: Update, context: CallbackContext) -> None:
    pass

def back_to_plov(update: Update, context: CallbackContext) -> None:
    pass

def back_to_salad(update: Update, context: CallbackContext) -> None:
    pass



def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END



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