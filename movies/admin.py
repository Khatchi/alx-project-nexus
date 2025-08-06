from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from movies.models import Movie, Rating, TrendingMovie, User, Watchlist

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
admin.site.register(Rating)
admin.site.register(Watchlist)
admin.site.register(TrendingMovie)
