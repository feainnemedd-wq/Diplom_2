import allure
import pytest
import requests
from urls import Urls
from data import ResponseMessages

class TestCreateOrder:

    @allure.title('Проверка создания заказа авторизованным пользователем')
    @allure.description('Авторизованный пользователь создает заказ с валидными ингредиентами. Ожидается статус 200.')
    def test_create_order_authenticated_success(self, create_user, get_ingredients):
        payload_user, user_data = create_user
        access_token = user_data.get('accessToken')
        
        ingredients = get_ingredients[:2]
        payload = {"ingredients": ingredients}
        
        response = requests.post(
            Urls.order_create, 
            headers={'Authorization': access_token}, 
            json=payload
        )
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Проверка создания заказа неавторизованным пользователем')
    @allure.description('Неавторизованный пользователь создает заказ. Ожидается статус 200.')
    def test_create_order_unauthenticated_success(self, get_ingredients):
        ingredients = get_ingredients[:2]
        payload = {"ingredients": ingredients}
        
        response = requests.post(Urls.order_create, json=payload)
        
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Ошибка при создании заказа без ингредиентов')
    @allure.description('Попытка создать заказ с пустым списком ингредиентов. Ожидается статус 400.')
    def test_create_order_empty_ingredients_error(self, login_user):
        payload = {"ingredients": []}
        
        response = requests.post(
            Urls.order_create, 
            headers={'Authorization': login_user}, 
            json=payload
        )
        
        assert response.status_code == 400
        assert response.json()['message'] == ResponseMessages.INGREDIENTS_REQUIRED

    @allure.title('Ошибка при создании заказа с неверным хешем ингредиента')
    @allure.description('Попытка создать заказ с несуществующим ID ингредиента. Ожидается статус 500.')
    def test_create_order_invalid_hash_error(self, login_user):
        payload = {"ingredients": ["invalid_hash_123_test"]}
        
        response = requests.post(
            Urls.order_create, 
            headers={'Authorization': login_user}, 
            json=payload
        )
        
        assert response.status_code == 500