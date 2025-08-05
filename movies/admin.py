from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'preferences')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('user_id', 'username', 'email', 'phone_number', 'created_at')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Movie)
