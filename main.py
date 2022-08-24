import os
import random

import requests
from dotenv import load_dotenv


def randomize_comic_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    random_comic_num = random.randint(0, response.json()['num']+1)

    return random_comic_num

def download_xkcd_picture():
    url = f'https://xkcd.com/{randomize_picture()}/info.0.json'
    response = requests.get(url)
    image_url = response.json()['img']
    comment = response.json()['alt']
    image_response = requests.get(image_url)

    response.raise_for_status()

    with open('image.jpg', "wb") as file:
        file.write(image_response.content)

    return comment

def get_server_inf(group_id, token, api_version):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id
    }
    response = requests.get(url, params=params)

    return response.json()['response']

def upload_server_picture(token, group_id, api_version):
    with open('image.jpg', 'rb') as file:
        url = get_server_inf(group_id, token, api_version)['upload_url']
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        photo = response.json()['photo']
        server = response.json()['server']
        hash = response.json()['hash']

    return photo, server, hash

def save_wall_photo(token, group_id, api_version):
    photo, server, hash = upload_server_picture(token, group_id, api_version)

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash,
        'access_token': token,
        'v': '5.131'
    }
    response = requests.post(url, params=params)

    photo_id = response.json()['response'][0]['id']
    owner_id = response.json()['response'][0]['owner_id']

    return photo_id, owner_id

def publication_comic(token, group_id, api_version):
    photo_id, owner_id = save_wall_photo(token, group_id, api_version)

    post_text = download_xkcd_picture()

    url = 'https://api.vk.com/method/wall.post'
    params =  {
        'v': api_version,
        'access_token': token,
        'owner_id': -int(group_id),
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': post_text,
        'from_group': 1
    }

    response = requests.post(url, params=params)

    return response.json()

def main():
    load_dotenv()

    group_id = os.getenv('GROUP_ID')
    api_version = os.getenv('API_VERSION', default='5.131')

    token = os.getenv('ACCESS_TOKEN')

    download_xkcd_picture()
    publication_comic(token,  group_id, api_version)


if __name__ == "__main__":
    main()