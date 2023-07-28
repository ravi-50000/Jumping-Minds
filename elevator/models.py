from django.db import models

# Create your models here.

class Elevator(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_elevator_working = models.BooleanField(default=True)
    current_floor = models.IntegerField(default=1)
    is_door_opened = models.BooleanField(default=False)
    is_door_closed = models.BooleanField(default=True)

class Requests(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name='requests')
    source_floor = models.IntegerField(null=True, blank=True)
    destination_floor = models.IntegerField(null=True, blank=True)
    is_elevator_moving_up = models.BooleanField()
