from rest_framework.serializers import ModelSerializer, Serializer

from base.models import Room

class RoomSerialzer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
