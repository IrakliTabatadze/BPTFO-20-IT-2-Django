from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import Event
from .serializers import EventSerializer

@api_view(['GET'])
def test(request):
    return Response({'Hello': 'World'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def event_list(request):
    events = Event.objects.all().order_by('-create_date')

    serializer = EventSerializer(events, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)