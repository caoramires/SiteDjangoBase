from django.contrib import admin
from .models import Framework, Dimension, Processo, Procedimento

# Register your models here.
admin.site.register(Framework)
admin.site.register(Dimension)
admin.site.register(Processo)
admin.site.register(Procedimento)