from django.contrib import admin

from .models import Client, ClientTag, ClientNetworkCode


for model in [Client, ClientTag, ClientNetworkCode]:
    admin.site.register(model)
