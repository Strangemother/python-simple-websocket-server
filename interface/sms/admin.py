from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.TextMessage)
admin.site.register(models.Receipt)
