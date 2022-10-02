from rest_framework import viewsets

from .serializers import *
from .models import *

class BannerViewSet(viewsets.ModelViewSet):
    queryset = SlidingBanner.objects.filter(hide=False)
    serializer_class = BannerSerializers
    lookup_field = 'slug'

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Links.objects.filter(hide=False)
    serializer_class = LinkSerializers

class InfoViewSet(viewsets.ModelViewSet):
    queryset = InfoTab.objects.filter(hide=False)
    serializer_class = InfoSerializers

