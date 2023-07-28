from elevator.serializers import CreateElevatorRequestSerializer, ElevatorRequestSerializer, ElevatorRequestResponseSerializer
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
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        number_of_elevations = validated_data.get('number_of_elevators')
        create_elevators = [Elevator() for _ in range(number_of_elevations)]
        Elevator.objects.bulk_create(create_elevators)
        return Response({'message': 'Successfully created Elevations'})
    
    @action(detail=False, methods=['post'], url_path='get_requests')
    def get_requests(self, request):
        serializer = ElevatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        elevator_number = validated_data.get('elevator_number')
        page_number = validated_data.get('page_number')
        elevator = get_object_or_404(Elevator, id=elevator_number)
        requests = Requests.objects.filter(elevator=elevator)
        
        if len(requests) == 0:
            return Response({'message':'No Requests for this Elevator till now'})
        
        page_obj, page_context = get_paginated_results(requests, page_number)
        
        result_list = []
        for request in page_obj.object_list:
            data = ElevatorRequestResponseSerializer(request).data
            data['id'] = str(request.id)
            result_list.append(data)
        
        result = {
            "page_context": page_context,
            "reviews": result_list
        }
        
        return Response({'result': result})
