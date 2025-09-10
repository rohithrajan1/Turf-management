from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password,make_password
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

class  UserSignUpView(APIView):  #create a user
    def post(self,request):
        try:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
                serializer.save()
                return Response({"message" : "User created sucessfully","username" : serializer.validated_data['username']})
            else:
                return Response(serializer.errors)
        except Exception as e:
            return (str(e))
        
class UserLoginView(APIView): #login user
    # def post(self, request):
    #     username = request.data.get('username')
    #     password = request.data.get('password')

    #     user = authenticate(username=username, password=password)
    #     if user:
    #         token, created = Token.objects.get_or_create(user=user)
    #         return Response({'token': token.key})
    #     else:
    #         return Response({'error': 'Invalid Credentials'})
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        else:
            return Response({'error': 'Invalid username or password'})

        


class BookingView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})  
        if serializer.is_valid():
            booking = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AdminTurfActionView(APIView):

    def post(self,request):
        try:
            serializer = TufSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response(str(e))
        
    def put(self,request,name):
        try:
            tuf = TufModel.objects.get(name=name)
            serializer = TufSerializer(tuf,data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response(str(e))
        
    def delete(self,request):
        data = request.data
        try:
            tuf_name = data.get('name')
            tuf = TufModel.objects.get(name = tuf_name)
            if tuf:
                tuf.delete()
                return Response({"message" : "Turf Deleted Sucessfully"})
            return Response({"message" : "Unable to delete the Turf"})
        except Exception as e:
            return Response(str(e))
