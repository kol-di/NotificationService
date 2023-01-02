from django.contrib import admin

from .models import Client, ClientTag, ClientNetworkCode, Message


for model in [Client, ClientTag, ClientNetworkCode, Message]:
    admin.site.register(model)
