from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Topics)
# admin.site.register(Units)
@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ("front_Side_Text", "back_Side_Text", "date_Modified", "added_By", "modified_By", "likes", "rank")
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        try:
            staff = User.objects.get(username=request.user.username)
            if(obj.added_By == None):
                obj.added_By = staff
            obj.modified_By = staff
        except User.DoesNotExist:              #if the post request is coming from User such as admin user
            pass
        super().save_model(request, obj, form, change)