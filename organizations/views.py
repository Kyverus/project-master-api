from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import OrganizationSerializer
from .models import Organization, OrganizationMembership

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
                return Response(status=status.HTTP_404_NOT_FOUND)