from django.contrib import admin

from mypass.models import *

admin.site.register(User)
admin.site.register(Password)
admin.site.register(Note)
admin.site.register(Address)
admin.site.register(Card)
admin.site.register(BankAccount)
admin.site.register(EncryptPassword)
