import allure
import pytest
import requests
from urls import Urls
from data import UsersData, ResponseMessages
from helpers import create_random_email, create_random_password, create_random_username, generate_user_payload

class TestRegistration:

    @allure.title('Проверка успешной регистрации аккаунта')
    def test_registration_new_account_success(self):
        payload = generate_user_payload()
        response = requests.post(Urls.user_register, json=payload)
        deserials = response.json()

        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'accessToken' in deserials
        
        access_token = deserials.get('accessToken')
        requests.delete(Urls.user_delete, headers={'Authorization': access_token})

    @allure.title('Проверка регистрации с незаполненным полем')
    @pytest.mark.parametrize('credentials', UsersData.credentials_with_empty_field)
    def test_registration_empty_field_error(self, credentials):
        response = requests.post(Urls.user_register, json=credentials)
        
        assert response.status_code == 403
        assert response.json()['message'] == ResponseMessages.REQUIRED_FIELDS

    @allure.title('Проверка регистрации уже существующего пользователя')
    def test_registration_duplicate_email_error(self):
        # 1. Создаем первого пользователя
        payload = generate_user_payload()
        first_response = requests.post(Urls.user_register, json=payload)
        access_token = first_response.json().get('accessToken')

        # 2. Пробуем зарегистрировать второго с тем же email
        duplicate_payload = generate_user_payload()
        duplicate_payload['email'] = payload['email']
        
        response = requests.post(Urls.user_register, json=duplicate_payload)

        # 3. Удаляем первого пользователя (очистка)
        requests.delete(Urls.user_delete, headers={'Authorization': access_token})

        assert response.status_code == 403
        assert response.json()['message'] == ResponseMessages.ALREADY_EXISTS