from django.contrib import admin
from .models import task

class taskadmin(admin.ModelAdmin):
    readonly_fields = ("created", )

# Register your models here.
admin.site.register(task, taskadmin)