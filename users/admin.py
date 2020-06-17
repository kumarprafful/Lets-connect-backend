from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from users.models import Contacts

User = get_user_model()

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'password',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important date'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined'),
        }),
    )
    list_display = ('first_name', 'last_name', 'email', 'date_joined',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

admin.site.register(Contacts)