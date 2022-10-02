from api.models import QuizSet, ClassModel
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Student(User):
    fullName = models.CharField(max_length=75)
    stdClass = models.ForeignKey(ClassModel, default=None ,blank=True,  null=True, on_delete=models.SET_DEFAULT)
    verified = models.BooleanField(default=False)
    eduright_Student = models.BooleanField(default=False, help_text="Whether the student is a student at Eduright.")

    class Meta:
        verbose_name= "Student"

class StudentMarksData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quizset = models.ForeignKey(QuizSet, on_delete=models.CASCADE, related_name="markModel_quizset")
    marksObtained = models.PositiveIntegerField()
    
    def __str__(self):
        return str(f"{self.student.fullName}_{self.quizset.setSlug}-{self.marksObtained}")

    class Meta:
        ordering=["-marksObtained"]