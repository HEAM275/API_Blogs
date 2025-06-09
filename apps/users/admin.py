# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_writer')
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {'fields': ('is_writer',)}),
    )


admin.site.register(User, CustomUserAdmin)
