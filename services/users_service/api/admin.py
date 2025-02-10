from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'is_active')
    list_filter = ('is_active', )
    list_editable = ('is_active',)
    list_display_links = ('first_name', 'last_name', 'username', 'email')
    search_fields = ('first_name', 'last_name', 'username', 'email')