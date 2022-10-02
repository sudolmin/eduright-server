from django.contrib import admin
from .models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("username", "fullName", "stdClass")

admin.site.register(StudentMarksData)

