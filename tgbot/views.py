import json
import logging
from django.views import View
from django.http import JsonResponse

from core.settings import DEBUG

logger = logging.getLogger(__name__)


def index(request):
    return JsonResponse({"url": "/tgadmin"})



