from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from drones.models import DroneCategory, Drone
from drones.serializers import DroneCategorySerializer
from drones.serializers import DroneSerializer
from drones.models import Pilot, Competition
from drones.serializers import PilotSerializer
from drones.serializers import PilotCompetitionSerializer
from drones.filters import CompetitionFilter
from drones import custom_permissions
from rest_framework.throttling import ScopedRateThrottle

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
    throttle_scope = "drones"
    throttle_classes = (ScopedRateThrottle,)
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
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.IsCurrentUserOwnerOrReadOnly,
    )
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    
    
class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = "drone-detail"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.IsCurrentUserOwnerOrReadOnly,
    )
    
    throttle_scope = "drones"
    throttle_classes = (ScopedRateThrottle,)

class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    throttle_scope = "pilots"
    throttle_classes = (ScopedRateThrottle,)
    name = "pilot_list"
    filterset_fields = ("gender", "races_count",)
    search_fields = ("^name", )
    ordering_fields = ("^name", "races_count")
    authentication_classes = (TokenAuthentication,) 
    permission_classes = (permissions.IsAuthenticated,)


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    throttle_scope = "pilots"
    throttle_classes = (ScopedRateThrottle,)
    name = "pilot-detail"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


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