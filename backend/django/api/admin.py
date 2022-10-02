from django.contrib import admin
from django.forms.widgets import Textarea
from .models import *

class AnswerInline(admin.TabularInline):
    model = Answer
    min_num=2
    max_num=5
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                            attrs={'rows': 8,
                                'cols': 50,})},
    }

class CategoryInline(admin.TabularInline):
    model = Category
    prepopulated_fields = {"subjectSlug": ("title","classModel",)}

admin.site.register(Staff)
admin.site.register(QuizSetTopic)
admin.site.register(QuestionTopic)

@admin.register(ClassModel)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("standard", "icon", "rank",)
    inlines = [
        CategoryInline,
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "rank", "subjectSlug")
    list_filter=("classModel",)
    prepopulated_fields = {"subjectSlug": ("title","classModel",)}

admin.site.register(QuizDifficulty)

@admin.register(QuizSet)
class QuizSetAdmin(admin.ModelAdmin):
    list_display = ("quizTitle", "max_marks", "mark_per_question", "negative_marking", "setSlug", "submitter", "set_Modifier", "date_created")
    list_filter=("difficulty", "quiztopic", "date_created","submitter",)
    search_fields=("setSlug", "quizTitle",)
    list_per_page = 50
    def save_model(self, request, obj, form, change):
        try:
            staff = Staff.objects.get(username=request.user.username)
            if(obj.submitter == None):
                obj.submitter = staff
            obj.set_Modifier = staff
        except Staff.DoesNotExist:              #if the post request is coming from User such as admin user
            pass
        super().save_model(request, obj, form, change)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]
    list_filter=("quesTopic", "lateX")
    search_fields=("quesText","quizset", )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                            attrs={'rows': 8,
                                'cols': 60,})},
    }

@admin.register(Topics)
class TopicsAdmin(admin.ModelAdmin):
    list_filter=("unit",)
    search_fields=("topic_Name","slug", )
    list_display = ("topic_Name", "slug")

@admin.register(Units)
class UnitsAdmin(admin.ModelAdmin):
    list_filter=("category",)

admin.site.register(Answer)
admin.site.site_header = "EduRight Admin Site"