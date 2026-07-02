# users/admin.py
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'state', 'city' , 'profession' , 'address', 'birth_date' , 'phone_number')
    list_filter = ('role', 'state')

admin.site.register(User, CustomUserAdmin)


