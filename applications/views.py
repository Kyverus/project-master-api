from django.shortcuts import get_object_or_404, render
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import OrganizationApplicationSerializer
from .models import OrganizationApplication
from organizations.models import Organization
from memberships.models import OrganizationMembership

# Create your views here.
@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def organizationApplications(request, orgpk):
    if request.method == "GET":
        organization = Organization.objects.get(id=orgpk)
        organizationMembers = OrganizationApplication.objects.filter(organization=organization)
        serializer = OrganizationApplicationSerializer(organizationMembers, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        organization = Organization.objects.get(id=orgpk)
        applicationSerializer = OrganizationApplicationSerializer(data=request.data)
        if OrganizationMembership.objects.filter(user=request.user, organization=organization).exists():
            raise serializers.ValidationError('User already is a member')
        if OrganizationApplication.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
        
        if applicationSerializer.is_valid():
            applicationSerializer.save(user=request.user, organization=organization)
            return Response(applicationSerializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['GET','PUT','DELETE'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def applicationObject(request, orgpk, applicationpk):
    if request.method == "GET":
        application = OrganizationApplication.objects.get(id=applicationpk)
        organization = Organization.objects.get(id=orgpk)
        if application.organization == organization:
            serializer = OrganizationApplicationSerializer(application, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "PUT":
        application = OrganizationApplication.objects.get(id=applicationpk)

        if application.user == request.user:
            serializer = OrganizationApplicationSerializer(data=request.data, instance=application)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Unauthorized request. You can only update your own application")


    if request.method == "DELETE":
        application = get_object_or_404(OrganizationApplication, pk=applicationpk)

        if application.user == request.user:
            application.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Unauthorized request. You can only delete your own application")
        
@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def acceptApplication(request, orgpk, applicationpk):
    if request.method == "POST":
        organization = get_object_or_404(Organization, pk=orgpk)

        if OrganizationMembership.objects.filter(user=request.user, organization=organization).exists():
            member = OrganizationMembership.objects.get(user=request.user, organization=organization)
        
            if member.owner or member.admin:
                application = get_object_or_404(OrganizationApplication, pk=applicationpk)

                OrganizationMembership.objects.create(user=application.user, organization=application.organization, owner=False, admin=False)
                application.delete()
                return Response("Application Accepted",status=status.HTTP_202_ACCEPTED)

        return Response("Unauthorized request. You should be the owner or an admin of this organization to accept applications")

@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def rejectApplication(request, orgpk, applicationpk):
    if request.method == "POST":
        organization = get_object_or_404(Organization, pk=orgpk)

        if OrganizationMembership.objects.filter(user=request.user, organization=organization).exists():
            member = OrganizationMembership.objects.get(user=request.user, organization=organization)
        
            if member.owner or member.admin:
                application = get_object_or_404(OrganizationApplication, pk=applicationpk)
                application.delete()
                return Response("Application Rejected",status=status.HTTP_202_ACCEPTED)

        return Response("Unauthorized request. You should be the owner or an admin of this organization to reject applications")
     

        