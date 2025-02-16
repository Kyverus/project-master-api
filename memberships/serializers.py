from rest_framework.serializers import ModelSerializer
from .models import OrganizationMembership

class OrganizationMembershipSerializer(ModelSerializer):
    class Meta:
        model = OrganizationMembership
        fields = '__all__'
