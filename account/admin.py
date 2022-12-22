from django.contrib import admin
from .models import User,Userinfo


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'integral')  # list
    search_fields = ('username',)
    fieldsets = (
        ['Main', {
            'fields': ('username', 'email'),
        }],
        ['Advance', {
            'classes': ('collapse',),
            'fields': ('integral','password'),
        }]

    )
admin.site.register(User,UserAdmin)
admin.site.register(Userinfo)
# Register your models here.
