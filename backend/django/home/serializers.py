
from rest_framework import serializers
from .models import *

class BannerSerializers(serializers.ModelSerializer):
    internal_link = serializers.ReadOnlyField(source='internal_Page.link')

    class Meta:
        model = SlidingBanner
        fields = ["title", 'image', 'plainShow', 'is_Internal_Link', 'internal_link', 'is_External_Link', "external_Link"]

class LinkSerializers(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = ["title","url","icon"]

class InfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = InfoTab
        fields = ["title","content","icon"]