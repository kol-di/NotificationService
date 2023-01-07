from django.contrib import admin

from .models import Mailing, Message


for model in [Mailing, Message]:
    admin.site.register(model)
