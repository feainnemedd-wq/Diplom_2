from helpers import create_random_email, create_random_password, create_random_username

class UsersData:
    
    # Данные для параметризации теста «регистрация с пустым полем»
    credentials_with_empty_field = [
        {'email': '', 'password': create_random_password(), 'name': create_random_username()},
        {'email': create_random_email(), 'password': '', 'name': create_random_username()},
        {'email': create_random_email(), 'password': create_random_password(), 'name': ''}
    ]

class IngredientData:
    burger_1 = [
        '61c0c5a71d1f82001bda4644', # Булка
        '61c0c5a71d1f82001bda464a'  # Начинка
    ]
    
    burger_2 = [
        '61c0c5a71d1f82001bda4644', 
        '61c0c5a71d1f82001bda464c'
    ]

    invalid_hash_ingredient = '61c0c5a71d1f82001bda464c_invalid'
    empty_ingredients = []

class ResponseMessages:
    ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INVALID_ID = "One or more ids provided are invalid"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"