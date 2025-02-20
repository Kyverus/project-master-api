from rest_framework.serializers import ModelSerializer
from .models import Membership

class MembershipSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'
