from django.contrib import admin
from clients.models import *


# Register your models here.
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'first_name', 'last_name', 'phone', 'user_id', 'avatar',
                    'birthday', 'level_id', 'scores')


class LevelsAdmin(admin.ModelAdmin):
    list_display = ('level_id', 'level_name')


admin.site.register(Client, ClientsAdmin)
admin.site.register(Level, LevelsAdmin)
