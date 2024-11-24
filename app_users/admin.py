from django.contrib import admin
from django.contrib.auth.models import Group

from .models import UserModel, Admin, Customer


admin.site.register(UserModel)
admin.site.unregister(Group)
admin.site.register(Admin)
admin.site.register(Customer)

