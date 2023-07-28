from elevator.serializers import CreateElevatorRequestSerializer, ElevatorRequestSerializer, ElevatorRequestResponseSerializer, ElevatorNextDestinationSerializer, ElevatorMovingUpOrDownSerializer
from elevator.models import Elevator, Requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from elevator.utils import get_paginated_results

# Create your views here.
class CreateElevatorView(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['post'], url_path='create_elevations')
    def create_elevations(self, request):
        serializer = CreateElevatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)            #Serialize the input if not valid throw exception for all api's
        validated_data = serializer.validated_data
        number_of_elevations = validated_data.get('number_of_elevators')
        create_elevators = [Elevator() for _ in range(number_of_elevations)]   #Create 'n' Elevators
        Elevator.objects.bulk_create(create_elevators)                         #Use Bulk Create to reduce DB calls
        return Response({'message': 'Successfully created Elevations'})
    
    @action(detail=False, methods=['post'], url_path='get_requests')
    def get_requests(self, request):
        serializer = ElevatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        page_number = validated_data.get('page_number')
        elevator = get_object_or_404(Elevator, id=elevator_number)     #Get the Object -> If yes process else throw exception with status code
        requests = Requests.objects.filter(elevator=elevator)
        
        if len(requests) == 0:
            return Response({'message':'No Requests for this Elevator till now'})   #If No requests made to the Elevator 'x'
        
        page_obj, page_context = get_paginated_results(requests, page_number)     #In order to send the whole data used Pagination for faster page load & reduced load on server
        
        result_list = []
        for request in page_obj.object_list:
            data = ElevatorRequestResponseSerializer(request).data           #Serialize the Model Data
            data['id'] = str(request.id)
            result_list.append(data)
        
        result = {
            "page_context": page_context,
            "reviews": result_list
        }
        
        return Response({'result': result})
    
    @action(detail=False, methods=['post'], url_path='next_destination')
    def next_destination(self, request):
        serializer = ElevatorNextDestinationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        
        request = Requests.objects.filter(elevator=elevator).order_by('-created_at').first()   #Get the Latest Request Entry
        if request is None:
            return Response({'message':'There is No Next Destination for this Elevator'})      #If No Entry
        if elevator.current_floor == request.destination_floor:
            return Response({'message': f'Elevator is stable on floor : {elevator.current_floor}'})    #If Elevator is Stable
        return Response(request.destination_floor)
    
    @action(detail=False, methods=['post'], url_path='moving_down_or_up')
    def moving_down_or_up(self, request):
        serializer = ElevatorMovingUpOrDownSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        request = Requests.objects.filter(elevator=elevator).order_by('-created_at').first()
        if request is None or request.destination_floor == elevator.current_floor:
            return Response({'message': "Elevator is Stable"})
        return Response({'message': "Moving Up" if request.is_elevator_moving_up == True else "Moving Down"})
