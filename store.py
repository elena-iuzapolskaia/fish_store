import json
import os

import requests
from dotenv import load_dotenv


def get_token(client_id):
    data = {
        'client_id': client_id,
        'grant_type': 'implicit'
    }

    response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    return response.json()['access_token']


def get_products(client_id):
    
    access_token = get_token(client_id)
    
    headers = {
        'Authorization': access_token,
    }

    response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    catalog = response.json()
    products = catalog['data']
    return products


def get_product(client_id, product_id):
    access_token = get_token(client_id)

    headers = {
        'Authorization': access_token,
    }

    response = requests.get(
        'https://api.moltin.com/v2/products/{}'.format(product_id),
        headers=headers
    )
    return response.json()['data']


def download_file(client_id, file_id):
    access_token = get_token(client_id)

    headers = {
        'Authorization': access_token,
    }

    response = requests.get(
        'https://api.moltin.com/v2/files/{}'.format(file_id),
        headers=headers
    )
    file_description = response.json()
    file_url = file_description['data']['link']['href']

    file = requests.get(file_url)

    return file_url


def create_customer(access_token):

    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json',
    }

    data = {
        "data": {
            "type": "customer",
            "name": "Ron Swanson",
            "email": "ron@swanson.com",
            "password": "mysecretpassword"
        }
    }

    response = requests.post('https://api.moltin.com/v2/customers', headers=headers, data=data)


def add_item_to_cart(client_id, product_id, cart_id, quantity):
    access_token = get_token(client_id)
    
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json',
    }

    data = {
        "data": {
            "id": product_id,
            "type": "cart_item",
            "quantity": quantity
        }
    }

    response = requests.post(
        'https://api.moltin.com/v2/carts/{}/items'.format(cart_id),
        headers=headers,
        json=data
    )


def get_cart_items(client_id, cart_id):
    access_token = get_token(client_id)

    headers = {
        'Authorization': access_token,
    }

    response = requests.get(
        'https://api.moltin.com/v2/carts/{}/items'.format(cart_id),
        headers=headers
    )
    return response.json()


def make_cart_description(cart):
    description = ''
    products = cart['data']
    
    for product in products:
        name = product['name']
        desc = product['description']
        price_per_kg = product['meta']['display_price']['with_tax']['unit']['formatted']
        quantity = product['quantity']
        total_price = product['meta']['display_price']['with_tax']['value']['formatted']
        description += f'{name}\n{desc}\n{price_per_kg} per kg\n{quantity}kg in cart for {total_price}\n\n'
    
    cart_price = cart['meta']['display_price']['with_tax']['formatted']
    
    description += f'Total: {cart_price}'
    return description


def main():
    load_dotenv()
    access_token = get_token(os.environ['CLIENT_ID'])
    cart_id = 1
    product_id = '85357a57-42d8-4219-9392-25f658dc438f'
    add_item_to_cart(access_token, product_id, cart_id)
    print(get_cart_items(access_token, 1))


if __name__ == '__main__':
    main()
