import hashlib
from api.models import Category, Topics
from django.contrib.auth.models import User
from django.db import models

class FlashCard(models.Model):
    topic = models.ForeignKey(Topics, default=0, on_delete=models.CASCADE, related_name="flashtopic")

    front_Side_Text = models.TextField(blank=True, null=True)
    front_Side_LateX = models.BooleanField(default=False, help_text="Whether the front side contain TeX format (default is \"False\").")
    front_Side_Image=models.ImageField(upload_to ='flashcard/', verbose_name="Flash Card Front Image", null=True, blank=True, help_text="Min size should be 128x128, and try not to exceed maximum size>100kb.")
    front_image_Size = models.PositiveIntegerField(default=200, help_text="Size of the image content on size. (Default is 200[in px])")

    back_Side_Text = models.TextField(blank=True, null=True)
    back_Side_LateX = models.BooleanField(default=False, help_text="Whether the back side contain TeX format (default is \"False\").")
    back_Side_Image=models.ImageField(upload_to ='flashcard/', verbose_name="Flash Card Back Image", null=True, blank=True, help_text="Min size should be 128x128, and try not to exceed maximum size>100kb.")
    back_image_Size = models.PositiveIntegerField(default=200, help_text="Size of the image content on size. (Default is 200[in px])")

    date_Modified = models.DateField(auto_now=True)
    added_By = models.ForeignKey(User, editable=False, null=True, blank=True, on_delete=models.SET_NULL, related_name="flashcardcreatedby")
    modified_By = models.ForeignKey(User, editable=False, null=True, blank=True, on_delete=models.SET_NULL, related_name="flashcardmodifiedby")

    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, blank=True, related_name='likedby',verbose_name="Liked By")

    datahash = models.CharField(max_length=32, null=True, blank=True, help_text="It will get calculated automatically")
    rank=models.IntegerField(default=0, help_text="The rank of flashcards will signify the order at which, flashcards will be shown in list view. Ex. rank 0 will be up rank 4 will be down. Default is 0.")
    
    def save(self, *args, **kwargs):
        hashStr = str(self.date_Modified)
        self.datahash = hashlib.md5(hashStr.encode()).hexdigest()
        if (self.id!=None):
            self.likes = self.liked_by.all().count()
        super(FlashCard, self).save(*args, **kwargs)
