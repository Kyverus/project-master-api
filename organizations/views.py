from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import OrganizationSerializer
from .models import Organization
from memberships.models import OrganizationMembership
# Create your views here.

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def organizationList(request):
    if request.method == "GET":
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        orgSerializer = OrganizationSerializer(data=request.data)
        # validating for already existing data
        if Organization.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
    
        if orgSerializer.is_valid():
            organization = orgSerializer.save()
            OrganizationMembership.objects.create(user=request.user, organization=organization, owner=True, admin=True)
            
            return Response(orgSerializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def organizationObject(request, pk):
    if request.method == "GET":
        organization = Organization.objects.get(id=pk)
        serializer = OrganizationSerializer(organization, many=False)
        return Response(serializer.data)
    
    if request.method == "PUT":
        organization = Organization.objects.get(id=pk)
        serializer = OrganizationSerializer(data=request.data, instance=organization)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        organizaton = get_object_or_404(Organization, pk=pk)
        organizaton.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    

    
    
