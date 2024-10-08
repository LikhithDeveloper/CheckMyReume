from django.contrib import admin
from .models import CustomUser,ResumeStorage
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ResumeStorage)