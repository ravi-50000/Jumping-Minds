from rest_framework import serializers

class CreateElevatorRequestSerializer(serializers.Serializer):
    number_of_elevators = serializers.IntegerField()
