class Urls:
    base_url = 'https://stellarburgers.education-services.ru'
    
    user_register = f'{base_url}/api/auth/register'
    user_auth = f'{base_url}/api/auth/login'
    user_update = f'{base_url}/api/auth/user'
    user_delete = f'{base_url}/api/auth/user'
    orders = f'{base_url}/api/orders'
    order_create = f'{base_url}/api/orders'
    ingredients = f'{base_url}/api/ingredients'
    get_user_orders = f'{base_url}/api/orders'