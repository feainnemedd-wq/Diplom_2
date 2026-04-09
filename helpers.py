from faker import Faker
import random

fake = Faker(locale='ru_RU')

def create_random_email():
    return fake.free_email()

def create_random_password():
    return fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

def create_random_username():
    return fake.first_name()

def generate_user_payload():
    return {
        "email": create_random_email(),
        "password": create_random_password(),
        "name": create_random_username()
    }

def generate_ingredients_payload(all_ingredients_list):
 

    if not all_ingredients_list:
        return {"ingredients": []}
    count = random.randint(1, 5)
    random_ingredients = random.sample(all_ingredients_list, k=min(count, len(all_ingredients_list)))
    
    return {"ingredients": random_ingredients}