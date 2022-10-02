from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginview),
    path('logout/', logoutview),
    path('get/', getokenview),
    path('create/', createUserView),
    path('deleteSAcc/', deleteAccount),
    path("profileQuery/", profiledetails),
    path("profileupdate/", changeAccountDetail),

    path('getclasslist/', getClasslist),
    path('getcategory/', getCategory),
    path('getHashes/', checksumData),
    path('checkattempt/', checkAttempt),
    path('savequizattempt/', saveQuizAttempt),
]