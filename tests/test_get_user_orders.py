import allure
import requests
import pytest
from urls import Urls

class TestGetOrders:

    @allure.title('Проверка успешного получения списка заказов авторизованного пользователя')
    @allure.description('Авторизованный пользователь запрашивает список своих заказов. Ожидается статус 200 и список заказов.')
    def test_get_orders_authenticated_user_success(self, create_order):
        access_token, order_data = create_order
        headers = {'Authorization': access_token}
        
        response = requests.get(Urls.get_user_orders, headers=headers)
        deserials = response.json()
        
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'orders' in deserials
        assert isinstance(deserials['orders'], list)

    @allure.title('Проверка получения списка заказов неавторизованным пользователем')
    def test_get_orders_unauthenticated_user_error(self):
        response = requests.get(Urls.get_user_orders)
        
        assert response.status_code == 401
        assert response.json() == {
            'success': False, 
            'message': 'You should be authorised'
        }