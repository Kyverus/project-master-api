from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from .serializers import ProjectSerializer

from .models import Project

# Create your views here.

@api_view(['GET', 'POST'])
def projectsList(request):
    if request.method == "GET":
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        project = ProjectSerializer(data=request.data)
        # validating for already existing data
        if Project.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
    
        if project.is_valid():
            project.save()
            return Response(project.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def projectObject(request, pk):
    if request.method == "GET":
        project = Project.objects.get(id=pk)
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)