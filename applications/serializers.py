from rest_framework.serializers import ModelSerializer
from .models import OrganizationApplication

class OrganizationApplicationSerializer(ModelSerializer):
    class Meta:
        model = OrganizationApplication
        fields = '__all__'
