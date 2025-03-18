from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from core.models import Event, EventImage
from .serializers import EventSerializer
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .filters import EventFilter
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 10

@api_view(['GET'])
def test(request):
    return Response({'Hello': 'World'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='GET',
    operation_summary='List All Events',
    operation_description='This function retrieve all events from database',
    manual_parameters=[
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('create_date_gte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('create_date_lte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    responses={
        status.HTTP_200_OK: EventSerializer,
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Bad Request',
            examples={'application/json': {'message': 'Bad Request'}},
        )
    }
)
@api_view(['GET'])
def event_list(request):
    result = cache.get('events')

    if not result:
        events = Event.objects.all().order_by('-create_date')

        filterset = EventFilter(request.query_params, queryset=events)

        if filterset.is_valid():
            events = filterset.qs

        paginator = CustomPagination()

        events = paginator.paginate_queryset(events, request)

        serializer = EventSerializer(events, many=True)

        result = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }


        cache.set('events', result, 30)

        print('Info selected from POSTGRES')

    else:
        print('Info selected from REDIS')

    return Response(result, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_summary='Create New Event',
    operation_description='this function created new event',
    manual_parameters=[
        openapi.Parameter(
            'images',
            openapi.IN_FORM,
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_FILE)
        )
    ],
    request_body=EventSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='Successfull Request',
            examples={'application/json': {'message': 'Event created successfully', 'data': {
                "id": 87,
                "title": "CBV - Class Based View Changed",
                "description": "CBV - Class Based View",
                "location": "meskhis_stationi",
                "start_date": None,
                "end_date": None,
                "create_date": "2025-03-07T21:27:47.275145",
                "update_date": "2025-03-07T21:52:06.987311",
                "max_attendees": 10000,
                "ticket_count": 10,
                "category": 1
            }}}
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: openapi.Response(
            description='Bad Request',
            examples={'application/json': {
                    "title": [
                        "This field is required."
                    ],
                    "description": [
                        "This field is required."
                    ],
                    "location": [
                        "This field is required."
                    ],
                    "max_attendees": [
                        "This field is required."
                    ],
                    "category": [
                        "This field is required."
                    ]
                }
            }
        )
    }
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        event = serializer.save()

        images = request.FILES.getlist('images')

        for image in images:
            EventImage.objects.create(event=event, image=image)

        return Response({'message': 'Event created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['PUT'])
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    event_serializer = EventSerializer(event, data=request.data)

    if event_serializer.is_valid():
        event_serializer.save()

        return Response({'message': f'Event with pk {pk} updated successfully', 'data': event_serializer.data}, status=status.HTTP_200_OK)

    return Response(event_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['DELETE'])
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    event.delete()

    return Response({'message': 'Event Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)