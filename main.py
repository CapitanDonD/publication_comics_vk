import os

import requests
from dotenv import load_dotenv
from pprint import pprint


GROUP_ID = os.getenv('GROUP_ID')

def download_xkcd_picture():
    url = 'https://xkcd.com/353/info.0.json'
    response = requests.get(url)
    image_url = response.json()['img']
    comment = response.json()['alt']
    image_response = requests.get(image_url)

    response.raise_for_status()

    with open('image.jpg', "wb") as file:
        file.write(image_response.content)

    return comment

def get_server_inf(group_id, token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': '5.131',
        'group_id': group_id
    }
    response = requests.get(url, params=params)

    return response.json()['response']

def upload_server_picture(token):
    with open('image.jpg', 'rb') as file:
        url = get_server_inf(GROUP_ID, token)['upload_url']
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        photo = response.json()['photo']
        server = response.json()['server']
        hash = response.json()['hash']

    return photo, server, hash

def save_wall_photo(token):
    photo, server, hash = upload_server_picture(token)

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': GROUP_ID,
        'server': server,
        'photo': photo,
        'hash': hash,
        'access_token': token,
        'v': '5.131'
    }
    response = requests.post(url, params=params)

    photo_id = response.json()['response']['id']
    owner_id = response.json()['response']['owner_id']

    return photo_id, owner_id

def publication_comic():

    url =


if __name__ == "__main__":
    load_dotenv()

    token = os.getenv('ACCESS_TOKEN')

    download_xkcd_picture()
    print(save_wall_photo(token))