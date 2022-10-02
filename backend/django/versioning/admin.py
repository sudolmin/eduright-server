from django.contrib import admin
from .models import *
from django.forms import Textarea
# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "language_Version", "area")

@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ("title", "Version", "slug")
    prepopulated_fields = {"slug": ("title","Version",)}

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("new_Feature_Title", "scale", "pending")
    list_filter=("pending", "scale")

@admin.register(Bugs)
class BugsAdmin(admin.ModelAdmin):
    list_display = ("title", "solved")
    list_filter=("solved",)

@admin.register(Security)
class SecurityAdmin(admin.ModelAdmin):
    list_display = ("future_Flaw_Warning", "niwaran", "solved")
    list_filter=("solved",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "release", "slug", "testing")
    list_filter=("release", "testing")
    prepopulated_fields = {"slug": ("title","release",)}
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                            attrs={'rows': 8,
                                'cols': 60,})},
    }