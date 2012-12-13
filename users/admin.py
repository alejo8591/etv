# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import UserProfile

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser: self.exclude.append('field_to_hide')
        return super(UserAdmin, self).get_form(request, obj, **kwargs) 

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)