from django.db import models

# Create your models here.
class Links(models.Model):
    title = models.CharField(max_length=50, help_text="Max Length is 50 characters.")
    url = models.URLField(max_length=250, help_text="Max Length is 250 characters.")
    icon=models.ImageField(upload_to ='impelinkicons/', verbose_name="Imp Link Icon", null=True, blank=True, help_text="Min size should be 128x128, and try not to exceed maximum size>25kb.")
    rank=models.IntegerField(default=0, help_text="The rank of class will signify the order at which,  images will be displayed. Default is 0.")
    hide = models.BooleanField(default=False, help_text="Don't show this in the app.")

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = 'Links'
        ordering = ('rank', )

        
    def __str__(self):
        return str(self.title)

class InternalPage(models.Model):
    title = models.CharField(max_length=50, help_text="Just for identifying. Max Length is 50 characters.")
    link =  models.CharField(max_length=30)

class SlidingBanner(models.Model):
    title = models.CharField(max_length=50, help_text="Just for identifying. Max Length is 50 characters.")
    hide = models.BooleanField(default=False, help_text="Don't show this in the app.")
    image=models.ImageField(upload_to ='homtabbanner/', verbose_name="Home Tab Banner Image", default='placeholder.png', null=True, blank=True, help_text="Min size should be 534x300, and try not to exceed maximum size>25kb.")
    plainShow = models.BooleanField(default=True, verbose_name="Is for show" ,help_text="Whether the image just for show only.")
    
    is_Internal_Link = models.BooleanField(default=True ,help_text="Whether the link leads to internal page of the app. If True fill the field below.")
    internal_Page = models.ForeignKey(InternalPage, null=True, blank=True, on_delete=models.CASCADE)

    is_External_Link = models.BooleanField(default=True ,help_text="Whether the link leads to any external links. If True fill the field below.")    
    external_Link = models.URLField(max_length=250, null=True, blank=True, help_text="any link ex: https://www.youtube.com/watch?v=aHjpOzsQ9YI")
    
    rank=models.IntegerField(default=0, help_text="The rank of class will signify the order at which, images will be displayed. Default is 0.")

    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Sliding Banner"
        verbose_name_plural = 'Sliding Banners'
        ordering = ('rank', )

    def __str__(self):
        return str(self.title)

class InfoTab(models.Model):
    title = models.CharField(max_length=50, help_text="Just for identifying. Max Length is 50 characters.")
    content = models.TextField()
    icon = models.ImageField(upload_to ='infotabsicons/', verbose_name="Imp Link Icon", null=True, blank=True, help_text="Min size should be 128x128, and try not to exceed maximum size>25kb.")
    hide = models.BooleanField(default=False, help_text="Don't show this in the app.")
    rank=models.IntegerField(default=0, help_text="The rank of class will signify the order at which, images will be displayed. Default is 0.")
    
    class Meta:
        verbose_name = "Information Tab"
        verbose_name_plural = 'Information Tab'
        ordering = ('rank', )

    def __str__(self):
        return str(self.title)