import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from models import Restaurant, Company


# воно мертвероджене ¯⁠\⁠_⁠(⁠ツ⁠)⁠_⁠/⁠¯

def xx():
    assert 1+1 == 2



# @pytest.fixture
# def api_client():
#     return APIClient()

# def test_get_restaurant_list(api_client):
#     url = reverse('company-home')
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK

# def test_create_restaurant(api_client):
#     url = reverse('create_restaurant')
#     company_id = 1
#     company = Company.objects.get(pk=company_id)
#     data = {'name': 'PyTest', 'address': 'PyTest', 'default_Meun': 'PyTestMenu','company': company }
#     response = api_client.post(url, data)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert Restaurant.objects.filter(name='PyTest').exists()   