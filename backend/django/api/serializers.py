from django.db.models import fields
from users.models import StudentMarksData
from rest_framework import serializers

from .models import *

class QuizSetTopicSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuizSetTopic
        fields = ['topicTitle']

class QuestionTopicSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuestionTopic
        fields = ['topicTitle']

class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['option', 'correct', 'lateX', "imageOption", "imageHeight"]

class QuestionSerializers(serializers.ModelSerializer):
    answers = AnswerSerializers(many=True)
    quesTopic = serializers.ReadOnlyField(source='quesTopic.topicTitle')
    difficulty = serializers.ReadOnlyField(source='difficulty.title')

    class Meta:
        model = Question
        fields = ["quesTopic", 'difficulty', 'quesText', 'answers', 'lateX', "imageQuestion", "imageHeight"]

class QuizSetSerializers(serializers.ModelSerializer):
    questions = QuestionSerializers(many=True)
    quiztopic = serializers.ReadOnlyField(source='quiztopic.topicTitle')
    difficulty = serializers.ReadOnlyField(source='difficulty.title')

    class Meta:
        model = QuizSet
        fields = ['quizTitle', "quiztopic", "difficulty", 'max_marks', 'mark_per_question', 'negative_marking', 'timeLimit',
        'description', 'setSlug', 'date_created', 'questions']

# // serializers for getting all info connected to topic

class TopicQuizSetSerializer(serializers.ModelSerializer):
    quiztopic = serializers.ReadOnlyField(source='quiztopic.topicTitle')

    class Meta:
        model = QuizSet
        fields = ['quizTitle', "quiztopic", 'max_marks', 'mark_per_question', 'negative_marking', 'setSlug']

class TopicSerializer(serializers.ModelSerializer):
    topicquizset = TopicQuizSetSerializer(many=True)
    class Meta:
        model= Topics
        fields = ['topic_Name', 'topicquizset']

# // serializers for getting all info connected to subjects
class CategoryQuizSetSerializer(serializers.ModelSerializer):
    quiztopic = serializers.ReadOnlyField(source='quiztopic.topicTitle')

    class Meta:
        model = QuizSet
        fields = ['quizTitle', "quiztopic", 'max_marks', 'mark_per_question', 'negative_marking', 'setSlug']

class CategorySerializer(serializers.ModelSerializer):
    categoryquizset = CategoryQuizSetSerializer(many=True)

    class Meta:
        model= Category
        fields = ['title', 'subjectSlug', 'categoryquizset']

# // serializers for info of marks obtained by students

class MarkSerializer(serializers.ModelSerializer):
    # markModel_quizset = serializers.RelatedField(many=True)
    student = serializers.ReadOnlyField(source='student.fullName')

    class Meta:
        model = StudentMarksData
        fields = ['student', 'marksObtained']

class MarksQuizSetSerializer(serializers.ModelSerializer):
    markModel_quizset = MarkSerializer(many=True)
    quiztopic = serializers.ReadOnlyField(source='quiztopic.topicTitle')

    class Meta:
        model = QuizSet
        fields = ["quizTitle", "quiztopic", "max_marks", "mark_per_question", "negative_marking", "setSlug", 'markModel_quizset']
