from django.contrib import admin

from  users_auth2.authentication.models import Profile
# Register your models here.
#admin.site.register(Profile)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    fields = ['user', 'bio']
