from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "auth_provider")

    def name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
