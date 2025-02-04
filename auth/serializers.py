from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }   
    

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]

        new_user = User.objects.create(username=username)
        new_user.set_password(password)
        new_user.save()

        return new_user