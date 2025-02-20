from django.shortcuts import get_object_or_404, render
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import ApplicationSerializer
from .models import Application
from organizations.models import Organization
from memberships.models import Membership

# Create your views here.
@api_view(['GET'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def applicationList(request):
    if request.method == "GET":
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def applicationObject(request, applicationpk):
    if request.method == "GET":
        application = Application.objects.get(id=applicationpk)
        serializer = ApplicationSerializer(application, many=False)
        return Response(serializer.data)
        
    if request.method == "PUT":
        application = Application.objects.get(id=applicationpk)
        if application.user == request.user:
            serializer = ApplicationSerializer(data=request.data, instance=application)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Unauthorized request. You can only update your own application")

    if request.method == "DELETE":
        application = get_object_or_404(Application, pk=applicationpk)
        if application.user == request.user:
            application.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Unauthorized request. You can only delete your own application")
        
@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def acceptApplication(request, applicationpk):
    if request.method == "POST":
        application = get_object_or_404(Application, pk=applicationpk)
        if Membership.objects.filter(user=request.user, organization=application.organization).exists():
            user_membership = Membership.objects.get(user=request.user, organization=application.organization)
            if user_membership.owner or user_membership.admin:
                Membership.objects.create(user=application.user, organization=application.organization, owner=False, admin=False)
                application.delete()
                return Response("Application Accepted",status=status.HTTP_202_ACCEPTED)
        return Response("Unauthorized request. You should be the owner or an admin of this organization to accept applications")

@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def rejectApplication(request, applicationpk):
    if request.method == "POST":
        application = get_object_or_404(Application, pk=applicationpk)
        if Membership.objects.filter(user=request.user, organization=application.organization).exists():
            user_membership = Membership.objects.get(user=request.user, organization=application.organization)
            if user_membership.owner or user_membership.admin:
                application.delete()
                return Response("Application Rejected",status=status.HTTP_202_ACCEPTED)
        return Response("Unauthorized request. You should be the owner or an admin of this organization to reject applications")
     

        