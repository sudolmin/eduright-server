import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.template.defaultfilters import default, random, slugify

AUTHKEY = "7vb3u_hfs88][d}#23'423[4'pkuadfsfsf"

class Staff(User):
    fullName = models.CharField(max_length=75)
    auth_Token = models.CharField(max_length=40, null=True, blank=True)
    class Meta:
        verbose_name= "Staff"
    def save(self, *args, **kwargs):
        authHash = str(self.fullName)+str(AUTHKEY)
        self.auth_Token = hashlib.md5(authHash.encode()).hexdigest()
        super(Staff, self).save(*args, **kwargs)

class ClassModel(models.Model):
    standard=models.CharField(max_length = 50)
    icon=models.ImageField(upload_to ='classicons/', default='default.png', verbose_name="Class Icon", null=True, blank=True, help_text="Min size should be 128x128, and try not to exceed maximum size>25kb.")
    rank=models.IntegerField(default=0, help_text="The rank of class will signify the order at which, classes will be shown in grid view. Ex. rank 0 will be up rank 4 will be down. Default is 0.")

    def __str__(self):
        return str(self.standard)

class Category(models.Model):
    classModel=models.ForeignKey(ClassModel, default=1, verbose_name="Class", on_delete=models.CASCADE)
    title=models.CharField(max_length = 50)
    icon=models.ImageField(upload_to ='categoryicons/', verbose_name="Category Icon", default='default.png', null=True, blank=True, help_text="Min size should be 128x128, and try not to exceed maximum size>25kb.")
    rank=models.IntegerField(default=0, help_text="The rank of category will signify the order at which, categories will be shown in grid view. Ex. rank 0 will be up rank 4 will be down. Default is 0.")
    subjectSlug = models.SlugField(unique=True, null=True, blank=True, help_text="You dont need to fill this field. It will be filled automatically")
    datahash = models.CharField(max_length=150, null=True, blank=True, help_text="It will get calculated automatically")
        
    def save(self, *args, **kwargs):
        if(self.icon==None):
            cateHash = str(self.subjectSlug)+str(self.rank)
        else:
            cateHash = str(self.subjectSlug)+str(self.icon.url)+str(self.rank)
        self.datahash = hashlib.md5(cateHash.encode()).hexdigest()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.classModel.standard+" "+self.title)

class Units(models.Model):
    category = models.ForeignKey(Category, default=0, on_delete=models.CASCADE, related_name="unitcategory")
    unit_Name = models.CharField(max_length=100)
    rank=models.IntegerField(default=0, help_text="The rank of unit will signify the order at which, units will be shown in list view. Ex. rank 0 will be up rank 4 will be down. Default is 0.")
    datahash = models.CharField(max_length=32, null=True, blank=True, help_text="It will get calculated automatically")
        
    def save(self, *args, **kwargs):
        hashStr = str(self.unit_Name)+str(self.rank)
        self.datahash = hashlib.md5(hashStr.encode()).hexdigest()
        super(Units, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.category.title + "-"+ self.unit_Name)

class Topics(models.Model):
    unit = models.ForeignKey(Units, default=0, on_delete=models.CASCADE, related_name="topicunit")
    topic_Name = models.CharField(max_length=100)
    rank=models.IntegerField(default=0, help_text="The rank of topic will signify the order at which, topics will be shown in list view. Ex. rank 0 will be up rank 4 will be down. Default is 0.")
    
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="You dont need to fill this field. It will be filled automatically")

    datahash = models.CharField(max_length=32, null=True, blank=True, help_text="It will get calculated automatically")
    
    def save(self, *args, **kwargs):
        hashStr = str(self.rank)+str(self.slug)
        self.slug = slugify(str(self.unit.category.classModel.id)+"-"+str(self.unit.category.id) + "-" + str(self.unit.id) + "-" + self.topic_Name)
        self.datahash = hashlib.md5(hashStr.encode()).hexdigest()
        super(Topics, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.unit.category.title + "-"+ self.unit.unit_Name + "-"+ self.topic_Name)

class QuizSetTopic(models.Model):
    topicTitle = models.CharField(max_length=50)
    def __str__(self):
        return str(self.topicTitle)

class QuizDifficulty(models.Model):
    title=models.CharField(max_length=20)
    def __str__(self):
        return str(self.title)

class QuizSet(models.Model):
    quiztopic = models.ForeignKey(QuizSetTopic, related_name='quizsettopics',verbose_name="Quiz Topic", null=True, blank=True, on_delete=models.SET_NULL)
    topic = models.ForeignKey(Topics, default=1, verbose_name="Topic", related_name='topicquizset',on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name="Category", related_name='categoryquizset',on_delete=models.CASCADE)
    difficulty = models.ForeignKey(QuizDifficulty, null=True, blank=True, verbose_name="Difficulty", related_name='difficultyquizset',on_delete=models.SET_NULL)
    quizTitle = models.CharField(max_length=50, verbose_name="Title")
    max_marks = models.PositiveIntegerField(null=True, blank=True)
    mark_per_question = models.PositiveIntegerField(null=True, blank=True)
    negative_marking = models.PositiveIntegerField(null=True, blank=True)
    timeLimit = models.PositiveIntegerField(null=True, blank=True, help_text="Time in seconds(e.g-15mins->15*60=900)")
    description = models.TextField(help_text="This description will be displayed when student will be given instructions for the quiz.", null=True, blank=True)
    setSlug = models.SlugField(unique=True, blank=True, null=True, help_text="You dont need to fill this field. It will be filled automatically")
    
    date_created = models.DateField(auto_now=True)
    submitter = models.ForeignKey(Staff, editable=False, null=True, blank=True, on_delete=SET_NULL, related_name="createdby")
    set_Modifier = models.ForeignKey(Staff, editable=False, null=True, blank=True, on_delete=SET_NULL, related_name="modifiedby")
    
    def save(self, *args, **kwargs):
        self.setSlug = slugify(self.quizTitle + "-" + str(self.id))
        super(QuizSet, self).save(*args, **kwargs)

    class Meta:
        ordering=["-date_created"]

    def __str__(self):
        return str(self.topic.unit.category.classModel.standard+" - "+self.topic.unit.category.title + " - " + self.topic.unit.unit_Name + " - " + self.topic.topic_Name + " - "+ self.quizTitle)

class QuestionTopic(models.Model):
    topicTitle = models.CharField(max_length=50)

    def __str__(self):
        return str(self.topicTitle)

class Question(models.Model):
    quesTopic = models.ForeignKey(QuestionTopic, related_name='questionTopics', verbose_name="Question Topic", null=True, blank=True, on_delete=models.SET_NULL)
    difficulty = models.ForeignKey(QuizDifficulty, null=True, blank=True, verbose_name="Difficulty", related_name='difficultyquestion',on_delete=models.SET_NULL)
    quizset= models.ManyToManyField(QuizSet, related_name='questions',verbose_name="Set Name")
    comment = models.CharField(max_length=75, null=True, blank=True, help_text="Example- [IIT-Mains 2019].")
    lateX = models.BooleanField(default=False, help_text="Whether the question contain TeX format (default is \"False\").")
    quesText = models.TextField(verbose_name="Question")
    imageQuestion=models.ImageField(upload_to ='questions/', verbose_name="Question Image", null=True, blank=True, help_text="Min size should be 128x128, and try not to exceed maximum size>100kb.")
    imageHeight = models.PositiveIntegerField(default=200, help_text="If the question contains image. The height of image can be adjusted here.(Default is 200[in px])")
    def __str__(self):
        return str(self.quesText)

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers',verbose_name="Question", on_delete=models.CASCADE)
    lateX = models.BooleanField(default=False, help_text="Whether the question contain TeX format (default is \"False\").")
    option = models.TextField(verbose_name="option", blank=True, null=True)
    correct = models.BooleanField(verbose_name="correct")
    imageOption=models.ImageField(upload_to ='answeroptions/', verbose_name="Option Image", null=True, blank=True, help_text="Min size should be 128x128, and try not to exceed maximum size>100kb.")
    imageHeight = models.PositiveIntegerField(default=100, help_text="If the answer contains image. The height of image can be adjusted here.(Default is 100[in px])")

    def __str__(self):
        return str(self.option)
