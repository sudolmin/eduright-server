import hashlib
from home.models import *
from api.models import QuizSet, ClassModel, Category
from users.models import Student, StudentMarksData
from django.http.response import JsonResponse
from django.middleware.csrf import get_token

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

SSN_USERID_KEY = "user_id"


def getClasslist(request):

    classOptionList = []

    for classobj in ClassModel.objects.order_by("-rank"):
        classDataDic = {}
        classDataDic["class"] = str(classobj.standard)
        if classobj.icon != None:
            classDataDic["icon"] = str(classobj.icon.url)
        else:
            classDataDic["icon"] = None

        classOptionList.append(classDataDic)

    return JsonResponse({"classDList": classOptionList})


def getCategory(request):

    className = request.POST['class']
    hashMode = request.POST["hashmode"]  # bool
    classObj = ClassModel.objects.get(standard=className)
    categoryObjs = Category.objects.filter(
        classModel=classObj).order_by("rank")

    if(hashMode == "true"):
        cateHash = ""
        for obj in categoryObjs:
            cateHash += str(obj.subjectSlug)+str(obj.icon.url)+str(obj.rank)
        cateHash = hashlib.md5(cateHash.encode()).hexdigest()
        return JsonResponse({"cateHash": cateHash})
    else:
        respList = []
        for obj in categoryObjs:
            dic = {}
            dic["title"] = obj.title
            dic["slug"] = obj.subjectSlug
            if obj.icon != None:
                dic["icon"] = str(obj.icon.url)
            else:
                dic["icon"] = None
            respList.append(dic)

        return JsonResponse({"categories": respList})


def getokenview(request):

    tok = get_token(request)
    html = "<html><body>%s</body></html>" % tok
    response = HttpResponse(html)

    return response


def loginview(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        request.session[SSN_USERID_KEY] = user.id
        response = JsonResponse(
            {'login': "true", "_usrID": request.session[SSN_USERID_KEY], "username": username})
    else:
        response = JsonResponse({'login': "false"})
    return response


def logoutview(request):
    rqstSSN = request.session[SSN_USERID_KEY]
    logout(request)
    return JsonResponse({'logout': "true", "sesiondata": rqstSSN})


def createUserView(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    fullname = request.POST['fullname']
    classInp = request.POST['class']

    successResponse = JsonResponse({'responseTitle': "The account has created Succesfully",
                                   "code": "UC200", "message": "You'll be redirected to the Sign In Page."})

    try:
        user = Student.objects.get(username=username)
        response = JsonResponse({'responseTitle': "The username already exist.",
                                "code": "UC400", "message": "Please try a different username."})
        return response
    except Student.DoesNotExist:
        user = Student.objects.create_user(
            username=username, email=email, password=password, fullName=fullname)

        userclass = ClassModel.objects.get(standard=classInp)
        user.stdClass = userclass
        user.save()
        return successResponse


def profiledetails(request):
    userID = request.session[SSN_USERID_KEY]

    try:
        userModel = Student.objects.get(pk=userID)

        username = userModel.username
        fullName = userModel.fullName
        email = userModel.email
        standard = userModel.stdClass.standard
        verified = userModel.verified
        edustd = userModel.eduright_Student

        resp = JsonResponse({"code": "PQ200", "profileInfo": {"username": username,
                                                              "fullname": fullName,
                                                              "email": email,
                                                              "standard": standard,
                                                              "verified": verified,
                                                              "edustd": edustd
                                                              }})
        return resp
    except Student.DoesNotExist:

        return JsonResponse({'code': "PQ400", "message": "User doesnot exist."})


def checksumData(request):
    user = Student.objects.get(pk=request.session[SSN_USERID_KEY])

    classData = ""
    catedata = ""
    for classEle in ClassModel.objects.all():
        classData += str(classEle.standard)
        categoryObjs = Category.objects.filter(classModel=classEle)
        for obj in categoryObjs:
            catedata += str(obj.datahash)

    for banEle in SlidingBanner.objects.filter(hide=False):
        banString = str(banEle.hide)+str(banEle.rank)+str(banEle.slug) + \
            str(banEle.image.url)+str(banEle.plainShow) + \
            str(banEle.external_Link)
        if(banEle.internal_Page != None):
            banString += str(banEle.internal_Page.title)

    infoString = ""
    for infoEle in InfoTab.objects.filter(hide=False):
        infoString = str(infoEle.title)+str(infoEle.content) + \
            str(infoEle.hide)+str(infoEle.icon.url)+str(infoEle.rank)

    linkString = ""
    for linkEle in Links.objects.filter(hide=False):
        linkString = str(linkEle.title)+str(linkEle.url) + \
            str(linkEle.hide)+str(linkEle.icon.url)+str(linkEle.rank)

    userData = user.username + user.fullName + user.stdClass.standard + user.email  + str(user.verified) + str(user.eduright_Student)
    userDataMsgDigest = hashlib.md5(userData.encode()).hexdigest()
    classDataMsgDigest = hashlib.md5(classData.encode()).hexdigest()
    cateDataMsgDigest = hashlib.md5(catedata.encode()).hexdigest()
    bannerDataMsgDigest = hashlib.md5(banString.encode()).hexdigest()
    infoDataMsgDigest = hashlib.md5(infoString.encode()).hexdigest()
    linkDataMsgDigest = hashlib.md5(linkString.encode()).hexdigest()

    return JsonResponse({'userDataMsgDigest': userDataMsgDigest, "classDataMsgDigest": classDataMsgDigest,
                        "cateDataMsgDigest": cateDataMsgDigest, "bannerDataMsgDigest": bannerDataMsgDigest,
                         "infoDataMsgDigest": infoDataMsgDigest, "linkDataMsgDigest": linkDataMsgDigest})


def checkAttempt(request):
    stdId = request.session[SSN_USERID_KEY]
    quizid = QuizSet.objects.get(setSlug=request.POST['quizSlug']).id

    response = JsonResponse({'attempted': True})
    try:
        StudentMarksData.objects.get(student=stdId, quizset=quizid)
    except StudentMarksData.DoesNotExist:
        response = JsonResponse({'attempted': False})

    return response


def saveQuizAttempt(request):
    stdId = request.session[SSN_USERID_KEY]
    stdObj = Student.objects.get(pk=stdId)

    quizObj = QuizSet.objects.get(setSlug=request.POST['quizSlug'])
    quizid = quizObj.id

    marks = int(request.POST['marks'])
    try:
        attempted = StudentMarksData.objects.filter(
            student=stdId, quizset=quizid)
        if(attempted.count() != 0):
            response = JsonResponse({'attempt saved': True})
        else:
            obj = StudentMarksData()

            obj.student = stdObj
            obj.quizset = quizObj
            obj.marksObtained = marks

            obj.save()
            response = JsonResponse({'attempt saved': True})
    except:
        response = JsonResponse({'attempt saved': False})

    return response


def changeAccountDetail(request):
    try:
        stdId = request.session[SSN_USERID_KEY]
        stdObj = Student.objects.get(pk=stdId)

        email = str(request.POST['email'])
        fullname = str(request.POST['fullname'])
        standard = str(request.POST['standard'])

        if(standard != ""):
            updatedClassObj = ClassModel.objects.get(standard=standard)
            stdObj.stdClass = updatedClassObj

        if(email != ""):
            stdObj.email = email

        if(fullname != ""):
            stdObj.fullName = fullname

        response = JsonResponse(
            {"code": "UP200", 'message': "Your Account has been updated successfully."})
        if(fullname != "" or email != "" or standard != ""):
            stdObj.save()

    except Student.DoesNotExist:
        response = JsonResponse(
            {"code": "UP404", 'message': "User doesnot exist."})

    return response


def deleteAccount(request):
    try:
        stdId = request.session[SSN_USERID_KEY]
        stdObj = Student.objects.get(pk=stdId)
        stdObj.delete()
        response = JsonResponse(
            {"code": "DSA200", 'message': "Your Account has been deleted successfully."})

    except Student.DoesNotExist:
        response = JsonResponse(
            {"code": "DSA404", 'message': "User doesnot exist."})
    return response
