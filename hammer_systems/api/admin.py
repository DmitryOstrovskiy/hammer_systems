from django.contrib import admin

from .models import User, ActivationCode, InviteCode


admin.site.register(User)
admin.site.register(ActivationCode)
admin.site.register(InviteCode)
