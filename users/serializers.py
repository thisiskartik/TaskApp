from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'country_code', 'phone_number', 'priority', 'date_joined', 'is_active')
