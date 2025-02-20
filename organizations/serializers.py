from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Organization
from memberships.models import Membership
from applications.models import Application
from django.urls import reverse

class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationApplicationSerializer(ModelSerializer):
    links = SerializerMethodField()
    
    def get_links(self, instance):
        return[
            self.get_retrieve_link(instance),
            self.get_update_link(instance),
            self.get_delete_link(instance)
        ]
    
    def get_retrieve_link(self, instance):
        return {
            "rel": "applications",
            "href": self.context['request'].build_absolute_uri(reverse("applications:application_object", kwargs={"applicationpk": instance.id})),
            "action": "GET",
        }

    def get_update_link(self, instance):
        return {
            "rel": "applications",
            "href": self.context['request'].build_absolute_uri(reverse("applications:application_object", kwargs={"applicationpk": instance.id})),
            "action": "UPDATE",
        }
    def get_delete_link(self, instance):
        return {
            "rel": "applications",
            "href": self.context['request'].build_absolute_uri(reverse("applications:application_object", kwargs={"applicationpk": instance.id})),
            "action": "DELETE",
        }

    class Meta:
        model = Application
        fields = ['id','user', 'organization', 'message', 'date', 'links']


class OrganizationMemberSerializer(ModelSerializer):
    links = SerializerMethodField()

    def get_links(self, instance):
        return[
            self.get_retrieve_link(instance),
            self.get_update_link(instance),
            self.get_delete_link(instance)
        ]
    
    def get_retrieve_link(self, instance):
        return {
            "rel": "memberships",
            "href": self.context['request'].build_absolute_uri(reverse("memberships:membership_object", kwargs={"membershippk": instance.id})),
            "action": "GET",
        }

    def get_update_link(self, instance):
        return {
            "rel": "memberships",
            "href": self.context['request'].build_absolute_uri(reverse("memberships:membership_object", kwargs={"membershippk": instance.id})),
            "action": "UPDATE",
        }
    def get_delete_link(self, instance):
        return {
            "rel": "memberships",
            "href": self.context['request'].build_absolute_uri(reverse("memberships:membership_object", kwargs={"membershippk": instance.id})),
            "action": "DELETE",
        }

    class Meta:
        model = Membership
        fields = ['id','user', 'organization', 'owner', 'admin', 'date', 'links']