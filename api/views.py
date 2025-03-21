from rest_framework.decorators import api_view, parser_classes, APIView
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
import hashlib
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView


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
    # result = cache.get('events')

    query_param_str = ''

    for k, v in request.query_params.items():
        query_param_str += f'{k}:{v}'

    cache_key = f'events_{hashlib.md5(query_param_str.encode()).hexdigest()}'


    result = cache.get(cache_key)

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


        cache.set(cache_key, result, 60)

        print('Info selected from POSTGRES')

    else:
        print('Info selected from REDIS')

    return Response(result, status=status.HTTP_200_OK)



# class EventListView(APIView):
#
#     @swagger_auto_schema(
#         operation_summary='List All Events',
#         operation_description='This function retrieve all events from database',
#         manual_parameters=[
#             openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
#             openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
#             openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#             openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#             openapi.Parameter('create_date_gte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#             openapi.Parameter('create_date_lte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
#         ],
#         responses={
#             status.HTTP_200_OK: EventSerializer,
#             status.HTTP_400_BAD_REQUEST: openapi.Response(
#                 description='Bad Request',
#                 examples={'application/json': {'message': 'Bad Request'}},
#             )
#         }
#     )
#     def get(self, request):
#         query_param_str = ''
#
#         for k, v in request.query_params.items():
#             query_param_str += f'{k}:{v}'
#
#         cache_key = f'events_{hashlib.md5(query_param_str.encode()).hexdigest()}'
#
#         result = cache.get(cache_key)
#
#         if not result:
#             events = Event.objects.all().order_by('-create_date')
#
#             filterset = EventFilter(request.query_params, queryset=events)
#
#             if filterset.is_valid():
#                 events = filterset.qs
#
#             paginator = CustomPagination()
#
#             events = paginator.paginate_queryset(events, request)
#
#             serializer = EventSerializer(events, many=True)
#
#             result = {
#                 'count': paginator.page.paginator.count,
#                 'next': paginator.get_next_link(),
#                 'previous': paginator.get_previous_link(),
#                 'results': serializer.data
#             }
#
#             cache.set(cache_key, result, 60)
#
#             print('Info selected from POSTGRES')
#
#         else:
#             print('Info selected from REDIS')
#
#         return Response(result, status=status.HTTP_200_OK)


class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        events = super().get_queryset()

        filterset = EventFilter(self.request.query_params, queryset=events)

        if filterset.is_valid():
            events = filterset.qs

        return events

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('create_date_gte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('create_date_lte', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        return super().get(request)

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


class EventCreateAPIView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        event = serializer.save()

        images = self.request.FILES.getlist('images')

        for image in images:
            EventImage.objects.create(event=event, image=image)

        return event

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'images',
                openapi.IN_FORM,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE)
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@api_view(['PUT'])
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    event_serializer = EventSerializer(event, data=request.data)

    if event_serializer.is_valid():
        event_serializer.save()

        return Response({'message': f'Event with pk {pk} updated successfully', 'data': event_serializer.data}, status=status.HTTP_200_OK)

    return Response(event_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class EventUpdateAPIView(UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass


@api_view(['DELETE'])
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    event.delete()

    return Response({'message': 'Event Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class EventDeleteAPIView(DestroyAPIView):
    queryset = Event.objects.all()



# JWT - JSON Web Token