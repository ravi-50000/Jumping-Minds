from elevator.serializers import CreateElevatorRequestSerializer
from elevator.models import Elevator, Requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

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
