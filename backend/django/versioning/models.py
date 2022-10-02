from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=20, unique=True)
    language = models.CharField(max_length=15)
    language_Version = models.CharField(max_length=10)
    area = models.CharField(max_length=20, help_text="Ex. Server-End, Front-End, Website, Application etc")

    def __str__(self):
        return str(self.name+" "+self.language+" "+self.language_Version)
        
class Packages(models.Model):
    title = models.CharField(max_length=30, help_text="Name of the dependency.")
    Version = models.CharField(max_length=10)
    use = models.CharField(max_length=100, null=True, blank=True, help_text="What does this package do. Max Characters: 100")
    implementation_Location = models.CharField(max_length=100, null=True, blank=True, help_text="Where is this package being implemented. Max Characters: 100")
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return str(self.title+" "+self.Version)
        
class Feature(models.Model):
    new_Feature_Title = models.CharField(max_length=100, unique=True, help_text="New feature that can be added to the app.")
    pending = models.BooleanField(default=True)
    scale = models.PositiveIntegerField(help_text="Impact on the app. Possible assumption.")
    explain_Scale_Rating = models.CharField(max_length=150, help_text="Explain what could be the impact of this new feature on the app. Max Characters: 150")
    drawbacks = models.CharField(max_length=100, null=True, blank=True, help_text="What drawback did/could this feature do.")
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ('-pending', )

    def __str__(self):
        if(self.pending):
            sText = "Not Done"
        else:
            sText = "Done"
        return str(self.new_Feature_Title+" - "+sText)

        
class Bugs(models.Model):
    title = models.CharField(max_length=20, unique=True, help_text="Max Characters: 20")
    comment = models.CharField(max_length=100, null=True, blank=True, help_text="Max Characters: 100")
    solved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        if(self.solved):
            sText = "Solved"
        else:
            sText = "Unsolved"
        return str(self.title+" - "+sText)

class Security(models.Model):
    future_Flaw_Warning = models.CharField(max_length=100, unique=True, help_text="Possible future security flaw in this version.")
    niwaran = models.CharField(max_length=100, null=True, blank=True, help_text="Possible solution for this security flaw.")
    solved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        if(self.solved):
            sText = "Solved"
        else:
            sText = "Unsolved"
        return str(self.title+" - "+sText)

class Product(models.Model):
    title = models.CharField(max_length=30)
    project = models.ForeignKey(Project, related_name="Product",on_delete=models.CASCADE)
    supports = models.CharField(max_length=30, null=True, blank=True, help_text="Supports Devices.")
    release = models.CharField(max_length=10)
    testing = models.BooleanField(default=False, verbose_name="Under Testing")
    slug = models.SlugField(unique=True)
    packages = models.ManyToManyField(Packages, blank=True, help_text="Packages included/removed.")
    feature = models.ManyToManyField(Feature, blank=True,)
    bugs = models.ManyToManyField(Bugs, blank=True,)
    security = models.ManyToManyField(Security, blank=True,)
    note = models.TextField(null=True, blank=True,)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        if(self.testing):
            sText = " Beta"
        else:
            sText = ""
        return str(self.title+" - "+ self.release + sText)