from rest_framework.serializers import ModelSerializer
from .models import SubTask


class SubTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = ('id', 'task', 'status', 'created_at', 'updated_at', 'deleted_at')
        extra_kwargs = {"status": {"required": False, "allow_null": True},
                        "task": {"required": False, "allow_null": True}}
