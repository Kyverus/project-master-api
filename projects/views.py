from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer

from .models import Project

# Create your views here.

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def projectsList(request):
    if request.method == "GET":
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        serializer = ProjectSerializer(data=request.data)
        # validating for already existing data
        if Project.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
    
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','PUT','DELETE'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def projectObject(request, pk):
    if request.method == "GET":
        project = Project.objects.get(id=pk)
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)

    if request.method == "PUT":
        project = Project.objects.get(id=pk)
        serializer = ProjectSerializer(data=request.data, instance=project)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status.HTTP_202_ACCEPTED)