from django.contrib import admin

from .models import TodoModel

# Register your models here.

class TodoAdminModel(admin.ModelAdmin):
    readonly_fields = ('added_on',)
 
admin.site.register(TodoModel,TodoAdminModel)




