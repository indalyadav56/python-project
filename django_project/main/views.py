from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class UserService:
    
    def __init__(self) -> None:
        print("INIALIZATION of user service..")
    
    def create_user(data: dict):
        
        with open('indal.txt', 'r') as file:
            contents = file.read()

        return Response({'message': 'successfully created user'+contents}, content_type='application/json')   

    def get_user(data: dict):
        return Response({'message': 'successfully get'})    
    
    def delete_user(data: dict):
        return Response({'message': 'successfully delete'}) 


class UserAPIView(APIView):
    
    def __init__(self):
        self.service = UserService()
    
    def post(self, request, *args, **kwargs):
        data = self.service.create_user()
        return data
    
    def get(self, request, *args, **kwargs):
        data = self.service.get_user()
        return data
    
    def delete(self, request, *args, **kwargs):
        data = self.service.delete_user()
        return data
    