import factory
import pytest
from django.urls import reverse

from . import UserFactory, ServiceAreaFactory
from ..models import ServiceArea


@pytest.mark.django_db
class TestUserListView:

    def test_get_user(self, api_client):
        users = UserFactory.create_batch(5)

        # Making a user admin user
        user = users[0]
        user.is_staff = True
        user.save()

        api_client.force_authenticate(user=user)
        url = reverse("api:user-list")
        response = api_client.get(url)
        assert response.status_code == 200

        assert len(response.data["results"]) == 5

    def test_creating_user(self, admin_client):
        data = {
            "name": "foo bar",
            "email": "foo@example.com",
            "password": "fffff",
            "phone_number": "+999999999"
        }
        url = reverse("api:user-list")
        response = admin_client.post(url, data)
        assert response.status_code == 201


@pytest.mark.django_db
class TestUserDetailsView:

    def test_get_user_details(self, admin_client):
        user = UserFactory()
        url = reverse("api:user-details", args=[user.id])
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_update_user_details(self, admin_client):
        user = UserFactory()
        url = reverse("api:user-details", args=[user.id])
        data = {"name": "foo"}
        response = admin_client.patch(url, data)
        assert response.status_code == 200

        user.refresh_from_db()
        assert user.name == "foo"

    def test_delete_user(self, admin_client):
        user = UserFactory()
        url = reverse("api:user-details", args=[user.id])
        response = admin_client.delete(url)
        assert response.status_code == 204


@pytest.mark.django_db
class TestServiceAreaListView:

    def test_get_service_area(self, provider_client):
        ServiceAreaFactory.create_batch(3)
        url = reverse("api:service-list")
        response = provider_client.get(url)
        assert response.status_code == 200

        assert len(response.data["results"]) == 3

    def test_filter_specific_location(self, provider_client):
        area = ServiceAreaFactory()
        lon, lat = area.area["coordinates"][0][0]

        url = reverse("api:service-list")
        url += f"?lat={lat}&lon={lon}"
        response = provider_client.get(url)
        assert response.status_code == 200

        assert len(response.data["results"]) == 1

    def test_create_service_area(self, provider_client):
        data = factory.build(dict, FACTORY_CLASS=ServiceAreaFactory)
        del data["created_by"]

        url = reverse("api:service-list")
        response = provider_client.post(url, data, format='json')
        assert response.status_code == 201

        assert ServiceArea.objects.all().count() == 1


@pytest.mark.django_db
class TestServiceAreaDetailsView:

    def test_get_service_area(self, provider_client):
        service_area = ServiceAreaFactory()
        url = reverse("api:service-details", args=[service_area.id])
        response = provider_client.get(url)
        assert response.status_code == 200

    def test_edit_service_area(self, provider_client):
        service_area = ServiceAreaFactory()
        url = reverse("api:service-details", args=[service_area.id])
        data = {"price": 100}
        response = provider_client.patch(url, data)
        assert response.status_code == 200

        service_area.refresh_from_db()
        assert service_area.price == 100

    def test_delete_service_area(self, provider_client):
        service_area = ServiceAreaFactory()
        url = reverse("api:service-details", args=[service_area.id])
        response = provider_client.delete(url)
        assert response.status_code == 204
