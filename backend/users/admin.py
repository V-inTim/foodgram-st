from django.contrib import admin
from .models import User, Subscribe
from django.contrib.auth.admin import UserAdmin


admin.site.register(Subscribe)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username')
