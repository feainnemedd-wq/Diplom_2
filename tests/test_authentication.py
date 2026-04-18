import allure
import pytest
import requests
from urls import Urls
from data import UserData, ResponseMessages
from helpers import generate_user_payload

class TestRegistration:

    @allure.title('Проверка успешной регистрации аккаунта')
    def test_registration_new_account_success(self):
        payload = generate_user_payload()
        
        with allure.step(f'Отправить POST запрос на регистрацию пользователя по адресу: {Urls.user_register}'):
            response = requests.post(Urls.user_register, json=payload)
        
        with allure.step('Проверить, что статус код 200 и в ответе есть токен доступа'):
            details = response.json()
            assert response.status_code == 200
            assert details['success'] is True
            assert 'accessToken' in details

        access_token = details.get('accessToken')
        
        with allure.step(f'Удалить созданного пользователя (очистка данных) по адресу: {Urls.user_delete}'):
            requests.delete(Urls.user_delete, headers={'Authorization': access_token})

    @allure.title('Проверка регистрации с незаполненным полем')
    @pytest.mark.parametrize('credentials', UserData.credentials_with_empty_field)
    def test_registration_empty_field_error(self, credentials):
        with allure.step(f'Отправить POST запрос с неполными данными (проверка обязательных полей) на {Urls.user_register}'):
            response = requests.post(Urls.user_register, json=credentials)
            
        with allure.step('Проверить, что сервер вернул ошибку 403 и верное сообщение'):
            assert response.status_code == 403
            assert response.json()['message'] == ResponseMessages.REQUIRED_FIELDS

    @allure.title('Проверка регистрации уже существующего пользователя')
    def test_registration_duplicate_email_error(self):
        payload = generate_user_payload()
        
        with allure.step('Предварительное условие: зарегистрировать первого пользователя'):
            first_response = requests.post(Urls.user_register, json=payload)
            access_token = first_response.json().get('accessToken')

        with allure.step('Попытка регистрации второго пользователя с тем же email'):
            duplicate_payload = generate_user_payload()
            duplicate_payload['email'] = payload['email']
            response = requests.post(Urls.user_register, json=duplicate_payload)

        with allure.step('Очистка: удалить первого пользователя'):
            if access_token:
                requests.delete(Urls.user_delete, headers={'Authorization': access_token})

        with allure.step('Проверить, что регистрация дубликата запрещена (статус 403)'):
            assert response.status_code == 403
            assert response.json()['message'] == ResponseMessages.ALREADY_EXISTS