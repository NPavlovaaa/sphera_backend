from django.contrib import admin
from users.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class UserInAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'password')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    search_field = 'username'


admin.site.register(User, UserInAdmin)
