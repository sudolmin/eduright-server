from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(InfoTab)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "rank", "hide")

@admin.register(Links)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "icon","rank", "hide")

admin.site.register(InternalPage)
@admin.register(SlidingBanner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "image", "plainShow", "is_Internal_Link", "is_External_Link", "hide")
    list_filter=("is_Internal_Link", "is_External_Link")
    prepopulated_fields = {"slug": ("title",)}