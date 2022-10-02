"""eduserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from api import urls as api_urls
from users import urls as users_urls
from home import urls as home_urls
from flashcardapp import urls as flashcard_urls
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('a3d4df7fcb0c2d32ffe08ddc82c1b51b/doc/', include('django.contrib.admindocs.urls')),    #a3d4df7fcb0c2d32ffe08ddc82c1b51b = md5("superadminsite")
    path('a3d4df7fcb0c2d32ffe08ddc82c1b51b/', admin.site.urls), #a3d4df7fcb0c2d32ffe08ddc82c1b51b = md5("superadminsite")
    path('87d2a024b2ae5674f2c091064a0c8cf2/', include(api_urls)),    # 87d2a024b2ae5674f2c091064a0c8cf2 = md5("restapiroute")
    path('9bc65c2abec141778ffaa729489f3e87/', include(users_urls)), #9bc65c2abec141778ffaa729489f3e87 = md5("users")
    path('c9027a676580cc6d5b4594afba86d126/', include(home_urls)), #c9027a676580cc6d5b4594afba86d126 = md5("homeapp")
    path('cd20e024128919bb3ef854f53a4f7e89/', include(flashcard_urls)), #cd20e024128919bb3ef854f53a4f7e89 = md5("flashcardapi")
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)