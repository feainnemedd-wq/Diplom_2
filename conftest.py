import pytest
import requests
from urls import Urls
from helpers import generate_user_payload

@pytest.fixture
def create_user():
    payload = generate_user_payload()
    response = requests.post(Urls.user_register, json=payload)
    user_data = response.json()
    
    yield payload, user_data
    
    token = user_data.get("accessToken")
    if token:
        requests.delete(Urls.user_delete, headers={"Authorization": token})

@pytest.fixture
def get_ingredients():
    response = requests.get(Urls.ingredients)
    if response.status_code == 200:
        ingredients_data = response.json().get("data", [])
        return [item["_id"] for item in ingredients_data]
    return []

@pytest.fixture
def login_user(create_user):
    payload, user_data = create_user
    return user_data.get("accessToken")

@pytest.fixture
def create_order(create_user, get_ingredients):
    payload_user, user_data = create_user
    token = user_data.get("accessToken")
    
    valid_ingredients = get_ingredients[:2]
    payload_order = {"ingredients": valid_ingredients}
    
    response = requests.post(
        Urls.order_create, 
        json=payload_order, 
        headers={"Authorization": token}
    )
    
    return token, response.json()