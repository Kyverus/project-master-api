from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import OrganizationMembershipSerializer
from .models import OrganizationMembership
from organizations.models import Organization

# Create your views here.
@api_view(['GET'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def organizationMembers(request, orgpk):
    if request.method == "GET":
        organization = Organization.objects.get(id=orgpk)
        organizationMembers = OrganizationMembership.objects.filter(organization=organization)
        serializer = OrganizationMembershipSerializer(organizationMembers, many=True)
        return Response(serializer.data)

@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def memberObject(request, orgpk, memberpk):
    if request.method == "GET":
        member = OrganizationMembership.objects.get(id=memberpk)
        organization = Organization.objects.get(id=orgpk)
        if member.organization == organization:
            serializer = OrganizationMembershipSerializer(member, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE":
        organization = get_object_or_404(Organization, pk=orgpk)

        if OrganizationMembership.objects.filter(user=request.user, organization=organization).exists():

            currentuser = OrganizationMembership.objects.get(user=request.user, organization=organization)

            member = OrganizationMembership.objects.get(id=memberpk)

            if member.owner:
                return Response("An owner cannot be removed from the organization, transfer ownership before leaving")

            if currentuser.owner or currentuser.admin or (currentuser.user == member.user):  

                member = get_object_or_404(OrganizationMembership, pk=memberpk)
                member.delete()
                return Response("Member Removed",status=status.HTTP_202_ACCEPTED)
                
        return Response("Unauthorized request. You should be the owner or an admin of this organization or the member itself to remove members")

@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def administratorStatusAddition(request, orgpk, memberpk):
    organization = get_object_or_404(Organization, pk=orgpk)

    if OrganizationMembership.objects.filter(user=request.user, organization=organization).exists():

        currentuser = OrganizationMembership.objects.get(user=request.user, organization=organization)
        member = OrganizationMembership.objects.get(id=memberpk)

        if not currentuser.owner:
            return Response("Unauthorized request. Only the owner can modify admin status")
    
        if member.admin:
            return Response("Member is already an administrator")
        else:
            member.admin = True
            member.save()
            return Response("Administration Status Added")

@api_view(['POST'])
@authentication_classes([JWTAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def administratorStatusRemoval(request, orgpk, memberpk):
    organization = get_object_or_404(Organization, pk=orgpk)

    if OrganizationMembership.objects.filter(user=request.user, organization=organization).exists():

        currentuser = OrganizationMembership.objects.get(user=request.user, organization=organization)
        member = OrganizationMembership.objects.get(id=memberpk)

        if not currentuser.owner:
            return Response("Unauthorized request. Only the owner can modify admin status")
        
        if member.admin:
            member.admin = False
            member.save()
            return Response("Administration Status Removed")
        else:
            return Response("Member is not an administrator")

