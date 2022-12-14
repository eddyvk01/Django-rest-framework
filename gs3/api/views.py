from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse ,JsonResponse
from .models import Student
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# for class based views
# @method_decorator(crsf_exempt, name='dispatch')
# class studentapi(view):
#  def get(self, request, *args, **kwargs): 

@csrf_exempt
def student_api(request):
    if request.method == 'GET':
        json_data = request.body  # data sending by clent(myapp.py file) to api 
        stream = io.BytesIO(json_data)  #kepting data as bytes in an in-memory buffer
        pythondata = JSONParser().parse(stream) #convert into python dictionary
        id = pythondata.get('id', None) #checking id is none or not
        if id is not None:
          stu = Student.objects.get(id=id)  #getting required data by using SQL query 
          serializer = StudentSerializer(stu)   #converting into python native datatype
          json_data = JSONRenderer().render(serializer.data)  #render into Json 
          return HttpResponse(json_data,content_type= 'application/json')
        
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many= True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type= 'application/json')

    if request.method =="POST":
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(data = pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg' : 'Data Created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type= 'application/json')
        
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type= 'application/json')

    if request.method =="PUT":
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id = id)
        serializer = StudentSerializer(stu, data = pythondata, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg' : 'Data Updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type= 'application/json')

    if request.method == "DELETE":
        json_data =request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id = id)
        stu.delete()
        res = {'msg' : 'Data Deleted'}
        # json_data = JSONRenderer().render(res)
        # return HttpResponse(json_data,content_type= 'application/json')
        return JsonResponse(res, safe= False)
        

        
         