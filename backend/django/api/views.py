import json
from django.http.response import JsonResponse
from rest_framework import viewsets

from .serializers import *
from .models import *

class QuizsetViewSet(viewsets.ModelViewSet):
    queryset = QuizSet.objects.all()
    serializer_class = QuizSetSerializers
    lookup_field = 'setSlug'
    
class MarksViewSet(viewsets.ModelViewSet):
    queryset = QuizSet.objects.all()
    serializer_class = MarksQuizSetSerializer
    lookup_field = 'setSlug'

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'subjectSlug'

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topics.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'id'

# api for POSTing quizsets and questions

from django.views.decorators.http import require_http_methods
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST"])
def PuttingQuizSet(request):
    postDict = json.loads(request.body.decode('utf-8'))

    # getting all data
    topicSlug = postDict['topicSlug']             #string field   (required)   (Slug for ForeignKey)
    title = postDict['quizTitle']                   #string field   (required)
    max_marks = postDict['ttl']
    mark_per_question = postDict['posi']
    negative_marks = postDict['nega']
    timeLimit = postDict['time']
    auth_token = postDict['auth_token']                 #string field   (required)  (ForeignKey)

    # get all the objects from the foreignKey
    topicObj = Topics.objects.get(slug=topicSlug)
    submitter = Staff.objects.get(auth_Token=auth_token)

    obj = QuizSet()

    # required field - no error handling
    obj.quizTitle = title
    obj.topic = topicObj
    obj.submitter = submitter
    obj.set_Modifier = submitter
    obj.max_marks = int(max_marks)
    obj.mark_per_question = int(mark_per_question)
    obj.negative_marking = int(negative_marks)
    obj.timeLimit = int(timeLimit)

    obj.save()
    obid = obj.id
    response = JsonResponse({"response":f'Quizset with title: {title} has been created in {topicSlug}', "id": obid})

    return response

@csrf_exempt
@require_http_methods(["POST"])
def PuttingQuestions(request):
    postDict = json.loads(request.body.decode('utf-8'))

    qDNExistList = []
    
    # getting all data
    quizsetidlist = postDict['quizsetidlist']     #list<str> field   (required)  (ManyToMany)
    quesText = postDict['quesText']                   #string field    (required)
    answers = postDict['answers']                     #list<dict> field   
    
    quesObj = Question()

    quesObj.quesText = quesText
    
    quesObj.save()

    for _qid in quizsetidlist:
        try:
            q=QuizSet.objects.get(id=_qid)
            quesObj.quizset.add(q)
        except QuizSet.DoesNotExist:
            qDNExistList.append(_qid)
            quizsetidlist.remove(_qid)

    for _a in answers:
        ansObj = Answer()
        ansObj.question = quesObj
        ansObj.option = _a['option']
        ansObj.correct = _a['correct']
        ansObj.save()

    response = JsonResponse({"response":f'Request Complete',"added": f"Question '{quesText}' is added to sets : {quizsetidlist}","except":f'{qDNExistList} sets doesnot exist please try adding them separately.'})
    
    return response