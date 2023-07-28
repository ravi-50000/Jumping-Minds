from rest_framework import serializers

class CreateElevatorRequestSerializer(serializers.Serializer):
    number_of_elevators = serializers.IntegerField()

class ElevatorRequestSerializer(serializers.Serializer):
    elevator_number = serializers.IntegerField()
    page_number = serializers.IntegerField()

class ElevatorRequestResponseSerializer(serializers.Serializer):
    source_floor = serializers.IntegerField()
    destination_floor= serializers.IntegerField()
    is_elevator_moving_up = serializers.BooleanField()
