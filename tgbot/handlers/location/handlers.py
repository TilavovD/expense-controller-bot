import telegram
from telegram import Update
from telegram.ext import CallbackContext

import geopy.distance

from tgbot.handlers.location.static_text import share_location, thanks_for_location
from tgbot.handlers.location.keyboards import send_location_keyboard
from tgbot.models import User, Location


def ask_for_location(update: Update, context: CallbackContext) -> None:
    """ Entered /ask_location command"""
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id,
        text=share_location,
        reply_markup=send_location_keyboard()
    )


def location_handler(update: Update, context: CallbackContext) -> None:
    # receiving user's location
    u = User.get_user(update, context)
    base_lat = 41.350448
    base_lon = 69.302703
    lat, lon = update.message.location.latitude, update.message.location.longitude
    
    coords_1 = (base_lat, base_lon)
    coords_2 = (lat, lon)
    
    distance = geopy.distance.distance(coords_1, coords_2).km

    
    Location.objects.create(user=u, latitude=lat, longitude=lon)

    update.message.reply_text(
        f"{distance}",
        reply_markup=telegram.ReplyKeyboardRemove(),
    )
