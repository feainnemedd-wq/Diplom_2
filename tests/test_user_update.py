import allure
import requests
from urls import Urls
from helpers import generate_user_payload

class TestUserUpdate:

    @allure.title('Проверка изменения данных авторизованного пользователя')
    def test_update_user_authenticated_success(self, create_user):
        payload, user_data = create_user
        access_token = user_data.get('accessToken')
        
        new_data = generate_user_payload()
        
        response = requests.patch(
            Urls.user_update, 
            headers={'Authorization': access_token}, 
            json=new_data
        )
        
        result = response.json()
        
        assert response.status_code == 200
        assert result['success'] is True
        assert result['user']['email'] == new_data['email'].lower()
        assert result['user']['name'] == new_data['name']

    @allure.title('Проверка изменения данных неавторизованного пользователя')
    def test_update_user_unauthenticated_error(self):
        new_data = generate_user_payload()
        
        response = requests.patch(Urls.user_update, json=new_data)
        
        assert response.status_code == 401
        assert response.json() == {
            'success': False, 
            'message': 'You should be authorised'
        }