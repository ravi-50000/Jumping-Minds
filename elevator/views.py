from elevator.serializers import CreateElevatorRequestSerializer, ElevatorRequestSerializer, ElevatorRequestResponseSerializer, ElevatorNextDestinationSerializer, ElevatorMovingUpOrDownSerializer, SaveElevatorRequestSerializer, ElevatorDestinationSerializer, ElevatorOpenOrCloseDoorSerializer, ElevatorNotWorkingSerializer, ElevatorWorkingSerializer
from elevator.models import Elevator, Requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from elevator.utils import get_paginated_results

# Create your views here.
class CreateElevatorView(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['post'], url_path='create_elevators')
    def create_elevations(self, request):
        serializer = CreateElevatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)            #Serialize the input if not valid throw exception for all api's
        validated_data = serializer.validated_data
        number_of_elevations = validated_data.get('number_of_elevators')
        create_elevators = [Elevator() for _ in range(number_of_elevations)]   #Create 'n' Elevators
        Elevator.objects.bulk_create(create_elevators)                         #Use Bulk Create to reduce DB calls
        return Response({'message': 'Successfully created Elevators'})
    
    @action(detail=False, methods=['post'], url_path='get_elevator_requests')
    def get_elevator_requests(self, request):
        serializer = ElevatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        page_number = validated_data.get('page_number')
        elevator = get_object_or_404(Elevator, id=elevator_number)     #Get the Object -> If yes process else throw exception with status code
        requests = Requests.objects.filter(elevator_id=elevator.id)
        
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
            "requests_list": result_list
        }
        
        return Response({'result': result})
    
    @action(detail=False, methods=['post'], url_path='next_destination')
    def next_destination(self, request):
        serializer = ElevatorNextDestinationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        
        request = Requests.objects.filter(elevator_id=elevator.id).order_by('-created_at').first()   #Get the Latest Request Entry
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
        if elevator.is_elevator_working == False:
            return Response({'message': "Oops! Elevator is not working"})   
        
        request = Requests.objects.filter(elevator_id=elevator.id).order_by('-created_at').first()
        if request is None or request.destination_floor == elevator.current_floor:
            return Response({'message': "Elevator is Stable"})
        return Response({'message': "Moving Up" if request.is_elevator_moving_up == True else "Moving Down"})

    @action(detail=False, methods=['post'], url_path='save_elevator_request')
    def save_elevator_request(self, request):
        serializer = SaveElevatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        current_floor = validated_data.get('current_floor')
        destination_floor = validated_data.get('destination_floor')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        
        if elevator.is_elevator_working == False:
            return Response({'message': "Oops! Elevator is not working"})     #Before Saving the Request Check if Elevator is Healthy or Not
        
        if current_floor == destination_floor:
            return Response({'message': "Current Floor & Destination Floor Should not be Same"})
        
        if not current_floor == elevator.current_floor:
            return Response({'message': f"Elevator Should Start from Floor: {elevator.current_floor}"})
        
        Requests.objects.create(
            elevator = elevator,
            source_floor = current_floor,
            destination_floor = destination_floor,
            is_elevator_moving_up = True if destination_floor>current_floor else False,
        )

        return Response({'message': "Successfully Created Request for Elevator"})
    
    @action(detail=False, methods=['post'], url_path='mark_elevator_not_working')
    def mark_elevator_not_working(self, request):
        serializer = ElevatorNotWorkingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        if elevator.is_elevator_working == False:
            return Response({'message': "Elevator Already in Not Working State"})
        elevator.is_elevator_working = False                            #Mark Elevator ‘x’ as not working
        elevator.save()
        return Response({'message': "Elevator Marked as Not Working"})
    
    @action(detail=False, methods=['post'], url_path='open_or_close_the_door')
    def open_or_close_the_door(self, request):
        serializer = ElevatorOpenOrCloseDoorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        open_door = validated_data.get('open_door')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        
        if elevator.is_elevator_working == False:
            return Response({'message': "Oops! Elevator is not working"})         #Before Opening/Closing the Door Check if Elevator is Healthy or Not
        
        if open_door == True:
            if elevator.is_door_opened == True:
                return Response({'message': "Elevator Door Already Opened"})
            
            elevator.is_door_opened = True
            elevator.is_door_closed = False
        else:
            if elevator.is_door_closed == True:
                return Response({'message': "Elevator Door Already Closed"})
            
            elevator.is_door_closed = True
            elevator.is_door_opened = False
            
        elevator.save()
        return Response({'message': "Elevator Door Opened" if open_door == True else "Elevator Door Closed"})
    
    @action(detail=False, methods=['post'], url_path='reached_elevator_destination')  #Extra API -> Update Current Floor if reached Destination
    def reached_elevator_destination(self, request):
        serializer = ElevatorDestinationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        destination_floor = validated_data.get('destination_floor')
        id = validated_data.get('id')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        request = get_object_or_404(Requests, elevator=elevator, id=id)
        if not request.destination_floor == destination_floor:
            return Response({'message': "Given Wrong Destination Floor"})
        elevator.current_floor = destination_floor
        elevator.save()
        
        return Response({'message': "Succesfully Reached Destination"})

    @action(detail=False, methods=['post'], url_path='mark_elevator_working')    #Extra API -> Mark Elevator 'x' as Working
    def mark_elevator_working(self, request):
        serializer = ElevatorWorkingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        if elevator.is_elevator_working == True:
            return Response({'message': "Elevator Already in Working State"})
        elevator.is_elevator_working = True                            #Mark Elevator ‘x’ as working
        elevator.save()
        return Response({'message': "Elevator Marked as Working"})
