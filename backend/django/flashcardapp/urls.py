from django.urls import path
from .views import *

urlpatterns = [
    path('getflashunit/', getFlashUnits),
    path('getflashtopic/', getFlashTopics),
    path('getflashcard/', getFlashCards),
    path('likeflashfunc/', likeflashfunc),
    path('postflashcard/', postflashcard),
    path('updateflashcard/', updateflashcard),
    path('deleteflashcard/', deleteflashcard),
]