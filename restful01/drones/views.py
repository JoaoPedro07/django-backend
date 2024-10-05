from django.shortcuts import render
from rest_framework import generics
from drones.models import DroneCategory, Drone
from drones.serializers import DroneCategorySerializer
from drones.serializers import DroneSerializer
from drones.models import Pilot, Competition
from drones.serializers import PilotSerializer
from drones.serializers import PilotCompetitionSerializer
from rest_framework import viewsets
from drones.filters import CompetitionFilter

# Create your views here.

class DroneCategoryViewSet(viewsets.ModelViewSet):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = "dronecategory_list"
    search_fields = ("^name",)
    ordering_fields = ("name",)


class DroneList(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = "drone_list"
    filterset_fields = (
        "drone_category",
        "has_it_competed",
    )
    search_fields = ("^name",)
    ordering_fields = (
        "name",
        "manufacturing_date",
    )
    
class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = "drone-detail"
    
    

class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = "pilot_list"
    filterset_fields = ("gender", "races_count",)
    search_fields = ("^name", )
    ordering_fields = ("^name", "races_count")

class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = "pilot-detail"


class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition_list"
    filterset_class = CompetitionFilter
    ordering_fields = (
        "distance_in_feet",
        "distance_achievement_date",
    )

class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = "competition-detail"