from rest_framework import serializers

class CreateElevatorRequestSerializer(serializers.Serializer):
    number_of_elevators = serializers.IntegerField(min_value=1,max_value=20) #Set the Elevators Range if want

class ElevatorRequestSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField(min_value=1,max_value=20)
    page_number = serializers.IntegerField()

class ElevatorRequestResponseSerializer(serializers.Serializer):
    source_floor = serializers.IntegerField(min_value=1)           #Assume Each Elevator Starts from First Floor
    destination_floor= serializers.IntegerField(min_value=1)
    is_elevator_moving_up = serializers.BooleanField()

class ElevatorNextDestinationSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField(min_value=1,max_value=20)

class ElevatorMovingUpOrDownSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField(min_value=1,max_value=20)

class ElevatorNotWorkingSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField(min_value=1,max_value=20)
    
class ElevatorDestinationSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField(min_value=1,max_value=20)
    destination_floor = serializers.IntegerField(min_value=1)
    id = serializers.IntegerField()
    
class ElevatorOpenOrCloseDoorSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField(min_value=1,max_value=20)
    open_door = serializers.BooleanField()
    
class SaveElevatorRequestSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField(min_value=1,max_value=20)
    current_floor = serializers.IntegerField(min_value=1)
    destination_floor = serializers.IntegerField(min_value=1)

class ElevatorWorkingSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField(min_value=1,max_value=20)
