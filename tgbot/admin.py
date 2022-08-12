from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from core.settings import DEBUG

from tgbot.models import Location
from tgbot.models import User
from tgbot.forms import BroadcastForm

from tgbot.handlers.broadcast_message.utils import _send_message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name',
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", ]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created_at']
