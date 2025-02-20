from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import MembershipSerializer
from .models import Membership
from organizations.models import Organization

# Create your views here.
@api_view(['GET'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def membershipList(request):
    if request.method == "GET":
        memberships = Membership.objects.all()
        serializer = MembershipSerializer(memberships, many=True)
        return Response(serializer.data)
    
@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def membershipObject(request, membershippk):
    if request.method == "GET":
        membership = Membership.objects.get(id=membershippk)
        serializer = MembershipSerializer(membership, many=False)
        return Response(serializer.data)
    
    if request.method == "DELETE":
        membership = get_object_or_404(Membership, pk=membershippk)
        if Membership.objects.filter(user=request.user, organization=membership.organization).exists():
            loggedin_member = Membership.objects.get(user=request.user, organization=membership.organization)
            if membership.owner:
                return Response("An owner cannot be removed from the organization, transfer ownership before leaving")
            if loggedin_member.owner or loggedin_member.admin or (loggedin_member.user == membership.user):  
                membership.delete()
                return Response("Member Removed",status=status.HTTP_202_ACCEPTED)       
        return Response("Unauthorized request. You should be the owner or an admin of this organization or the member itself to remove members")

@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def administratorStatusAddition(request, orgpk, membershippk):
    organization = get_object_or_404(Organization, pk=orgpk)
    if Membership.objects.filter(user=request.user, organization=organization).exists():
        user_membership = Membership.objects.get(user=request.user, organization=organization)
        membership = Membership.objects.get(id=membershippk)
        if not user_membership.owner:
            return Response("Unauthorized request. Only the owner can modify admin status")
        if membership.admin:
            return Response("Member is already an administrator")
        else:
            membership.admin = True
            membership.save()
            return Response("Administration Status Added")
        
@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def administratorStatusRemoval(request, orgpk, membershippk):
    organization = get_object_or_404(Organization, pk=orgpk)
    if Membership.objects.filter(user=request.user, organization=organization).exists():
        user_membership = Membership.objects.get(user=request.user, organization=organization)
        membership = Membership.objects.get(id=membershippk)
        if not user_membership.owner:
            return Response("Unauthorized request. Only the owner can modify admin status")
        if membership.admin:
            membership.admin = False
            membership.save()
            return Response("Administration Status Removed")
        else:
            return Response("Member is not an administrator")

