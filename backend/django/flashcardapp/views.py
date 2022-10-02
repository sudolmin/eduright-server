from users.models import Student
from .models import *
from api.models import Category, Units, Topics
from django.http.response import JsonResponse

# Create your views here.
SSN_USERID_KEY = "user_id"

def getFlashUnits(request):
    cateSlug = request.POST['cateslug']

    unitList = []
    unitObj = {}
    try:
        cateObj = Category.objects.get(subjectSlug=cateSlug)

        fUnitObjs=Units.objects.filter(category=cateObj).order_by("rank")
        
        for fObj in fUnitObjs:
            unitObj = {}
            unitObj["id"] = fObj.id
            unitObj["name"] = fObj.unit_Name
            
            unitList.append(unitObj)

        response = JsonResponse({'code':'FU200','responseTitle': "The unit exists.", "unitlist":unitList})

    except Category.DoesNotExist:
        response = JsonResponse({'code':'FU404','responseTitle': "The unit does not exist."})

    return response

def getFlashTopics(request):
    unitid = request.POST['unitid']

    topicList = []
    topicObj = {}
    try:
        unitObj = Units.objects.get(id=unitid)

        ftopicObjs=Topics.objects.filter(unit=unitObj).order_by("rank")
        
        for fObj in ftopicObjs:
            topicObj = {}
            topicObj["id"] = fObj.id
            topicObj["name"] = fObj.topic_Name
            
            topicList.append(topicObj)

        response = JsonResponse({'code':'FU200','responseTitle': "The topic exists.", "topiclist":topicList})

    except Units.DoesNotExist:
        response = JsonResponse({'code':'FU404','responseTitle': "The topic does not exist."})

    return response

def getFlashCards(request):
    topicid = request.POST['topicid']
    userID= request.session[SSN_USERID_KEY]

    cardList = []
    try:
        topicObj = Topics.objects.get(id=topicid)

        fcardObjs=FlashCard.objects.filter(topic=topicObj).order_by("rank")
        
        for fObj in fcardObjs:
            cardObj = {}
            cardObj["id"] = fObj.id
            cardObj["front_Text"] = fObj.front_Side_Text
            cardObj["front_LateX"] = fObj.front_Side_LateX            
            cardObj["front_size"] = fObj.front_image_Size
            cardObj["back_Text"] = fObj.back_Side_Text
            cardObj["back_LateX"] = fObj.back_Side_LateX
            cardObj["back_size"] = fObj.back_image_Size
            cardObj["likes"] = fObj.liked_by.all().count()
            cardObj["addedby"] = fObj.added_By.username

            cardObj["front_image"]=None
            cardObj["back_image"]=None

            if bool(fObj.front_Side_Image) == True:
                cardObj["front_image"]=str(fObj.front_Side_Image.url)
            if bool(fObj.back_Side_Image) == True:
                cardObj["back_image"]=str(fObj.back_Side_Image.url)

            try:
                stdobj=Student.objects.get(username=fObj.added_By.username)
                if stdobj.eduright_Student:
                    cardObj["edustd"]=True
                else:
                    cardObj["edustd"]=False

            except Student.DoesNotExist:
                cardObj["edustd"]=False

            
            likedbyuser = False
            if fObj.liked_by.filter(id=userID).count() == 1:
                likedbyuser = True

            cardObj['likedbyuser'] = likedbyuser


            cardList.append(cardObj)

        response = JsonResponse({'code':'FU200','responseTitle': "The card exists.", "cardlist":cardList})

    except Topics.DoesNotExist:
        response = JsonResponse({'code':'FU404','responseTitle': "The card does not exist."})

    return response

def likeflashfunc(request):
    flashid = request.POST['flashid']
    mode = request.POST['mode']
    userID= request.session[SSN_USERID_KEY]

    try:
        flashObj = FlashCard.objects.get(id=flashid)
        user = User.objects.get(pk=userID)
        if mode == "like":
            flashObj.liked_by.add(user)
            response = JsonResponse({'code':'FU200','responseTitle': "Card liked"})
        else:
            flashObj.liked_by.remove(user)
            response = JsonResponse({'code':'FU200','responseTitle': "Card disliked"})

        flashObj.save()

    except Topics.DoesNotExist:
        response = JsonResponse({'code':'FU404','responseTitle': "The card does not exist."})

    return response

def postflashcard(request):
    topicid = request.POST['topicid']
    front_Side_Text = request.POST['front_Text']
    front_Side_LateX = request.POST['front_LateX']
    back_Side_Text = request.POST['back_Text']
    back_Side_LateX = request.POST['back_LateX']
    userID= request.session[SSN_USERID_KEY]

    fObj = FlashCard()

    tpObj = Topics.objects.get(id=topicid)

    fObj.added_By=User.objects.get(id=userID)
    fObj.modified_By=User.objects.get(id=userID)
    fObj.topic = tpObj
    fObj.front_Side_Text = front_Side_Text
    if front_Side_LateX == "true":
        fObj.front_Side_LateX = True
    elif front_Side_LateX == "false":
        fObj.front_Side_LateX = False
    else:
        fObj.front_Side_LateX = front_Side_LateX

    fObj.back_Side_Text = back_Side_Text
    if back_Side_LateX == "true":
        fObj.back_Side_LateX = True
    elif back_Side_LateX == "false":
        fObj.back_Side_LateX = False
    else:
        fObj.back_Side_LateX = back_Side_LateX

    fObj.save()

    return JsonResponse({"response":"The flashcard is saved successfully"})

def updateflashcard(request):
    flashid = request.POST['flashid']
    front_Side_Text = request.POST['front_Text']
    front_Side_LateX = request.POST['front_LateX']
    back_Side_Text = request.POST['back_Text']
    back_Side_LateX = request.POST['back_LateX']
    userID= request.session[SSN_USERID_KEY]

    fObj = FlashCard.objects.get(id=flashid)

    fObj.modified_By=User.objects.get(id=userID)
    fObj.front_Side_Text = front_Side_Text
    if front_Side_LateX == "true":
        fObj.front_Side_LateX = True
    elif front_Side_LateX == "false":
        fObj.front_Side_LateX = False
    else:
        fObj.front_Side_LateX = front_Side_LateX

    fObj.back_Side_Text = back_Side_Text
    if back_Side_LateX == "true":
        fObj.back_Side_LateX = True
    elif back_Side_LateX == "false":
        fObj.back_Side_LateX = False
    else:
        fObj.back_Side_LateX = back_Side_LateX

    fObj.save()

    return JsonResponse({"response":"The flashcard is updated successfully"})

def deleteflashcard(request):
    flashid = request.POST['flashid']
    userID= request.session[SSN_USERID_KEY]

    FlashCard.objects.get(id=flashid).delete()

    return JsonResponse({"response":"The flashcard is deleted successfully"})