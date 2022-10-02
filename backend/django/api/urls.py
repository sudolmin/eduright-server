from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'quizapi', QuizsetViewSet)
# router.register(r'batchinfo', BatchSetViewSet)
router.register(r'marksinfo', MarksViewSet)
router.register(r'categoryinfo', CategoryViewSet)
router.register(r'topicapi', TopicViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('putquizsets/', PuttingQuizSet),
    path('puttingquestion/', PuttingQuestions),
]