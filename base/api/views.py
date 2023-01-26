from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.serializers import ModelSerializer, Serializer
from .serializers import RoomSerialzer
from base.models import Room
import json



@api_view(['GET'])
def getData(request):

    Bool = request.user.is_authenticated

    data = [
        'GET /api',
        'GET /api/rooms'
    ]

    rooms = Room.objects.all()
    ser = RoomSerialzer(rooms, many=True)

   
    return JsonResponse(data, safe=False)

