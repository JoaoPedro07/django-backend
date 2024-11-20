from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import DroneCategory, Pilot
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from . import views
# Create your tests here.
class DroneCategoryTests(APITestCase):
    def post_drone_category(self, name):
        url = reverse("dronecategory-list")
        data = {"name":name}
        response = self.client.post(url, data, format="json")
        return response
    
    def test_post_and_get_drone_category(self):
        new_drone_category_name = "Hexacopter"
        response = self.post_drone_category(new_drone_category_name)
        print("PK: {0}".format(DroneCategory.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert DroneCategory.objects.count() == 1
        assert DroneCategory.objects.get().name == new_drone_category_name
        
    def test_post_existing_drone_category_name(self):
        new_drone_category_name = "Duplicated Copter"
        response1 = self.post_drone_category(new_drone_category_name)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_drone_category(new_drone_category_name)
        print(response2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_get_drone_categories_collection(self):
        new_drone_category_name = "Super Copter"
        self.post_drone_category(new_drone_category_name)
        url = reverse("dronecategory-list")
        response = self.client.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == new_drone_category_name
        
    def test_update_drone_category(self):
        drone_category_name = "Category Initial Name"
        response = self.post_drone_category(drone_category_name)
        url = reverse("dronecategory-detail", args=[response.data["pk"]])
        updated_drone_category_name = "Updated  Name"
        data = {"name":updated_drone_category_name}
        patch_response = self.client.patch(url, data, format="json")
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data["name"] == updated_drone_category_name
        
        
class PilotDetailTests(APITestCase):
    def create_user_and_set_token_credentials(self):
        user = User.objects.create_user("user01", "user01@example.com", "user01P4ssw0rD")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {0}".format(token.key))
        
    def setUp(self):
        self.create_user_and_set_token_credentials()
        self.pilot = Pilot.objects.create(name="Guston", gender=Pilot.MALE, races_count=5)
        
    def test_get_pilot(self):
        url = reverse(views.PilotDetail.name, None, {self.pilot.pk})
        authorized_get_response = self.client.get(url, format="json")
        assert authorized_get_response.status_code == status.HTTP_200_OK
        assert authorized_get_response.data["name"] == self.pilot.name