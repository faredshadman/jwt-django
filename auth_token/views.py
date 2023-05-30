from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed 
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
import jwt, datetime
class Register(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
 
class Login(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")
        payload = {
            "id":user.id,
            "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            "iat":datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret', algorithm='HS256')
        
        response = Response()
        
        response.data = {
            "jwt":token
        }
        
        return response

            
class UserView(APIView):
    def post(self,request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        user = User.objects.filter(id=payload['id']).first()
        print(user)
        serializer = UserSerializer(user)
                
        return Response(serializer.data)
        