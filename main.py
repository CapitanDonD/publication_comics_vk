import os
import random

import requests
from dotenv import load_dotenv


def randomize_comic_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    random_comic_num = random.randint(0, response.json()['num']+1)

    return random_comic_num

def download_xkcd_comic():
    url = f'https://xkcd.com/{randomize_comic_number()}/info.0.json'
    response = requests.get(url)
    image_url = response.json()['img']
    comment = response.json()['alt']
    image_response = requests.get(image_url)

    response.raise_for_status()

    try:
        with open('image.jpg', "wb") as file:
            file.write(image_response.content)
        os.remove('image.jpg')
    except ValueError:
        print('Файл не удалось загрузить. Проверьте ссылку или запрос на правильность составления.')

    return comment

def get_comic_inf(group_id, token, api_version):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': api_version,
        'group_id': group_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()['response']['upload_url']

def upload_server_comic(url):
    with open('image.jpg', 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
    unpack_response = response.json()
    photo = unpack_response['photo']
    server = unpack_response['server']
    photo_hash = unpack_response['hash']

    return photo, server, photo_hash

def save_wall_comic(photo, server, hash, group_id, token, api_version):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash,
        'access_token': token,
        'v': api_version
    }
    response = requests.post(url, params=params)
    response.raise_for_status()

    unpack_response = response.json()

    photo_id = unpack_response['response'][0]['id']
    owner_id = unpack_response['response'][0]['owner_id']

    return photo_id, owner_id

def publicate_comic(token, group_id, api_version, owner_id, photo_id):
    post_text = download_xkcd_comic()

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
    response.raise_for_status()

    return response.json()

def main():
    load_dotenv()

    group_id = os.getenv('GROUP_ID')
    api_version = os.getenv('API_VERSION', default='5.131')
    vk_implicit_flow_token = os.getenv('VK_IMPLICIT_FLOW_TOKEN')

    upload_url = get_comic_inf(group_id, vk_implicit_flow_token, api_version)
    photo, server, photo_hash = upload_server_comic(upload_url)
    photo_id, owner_id = save_wall_comic(photo, server, photo_hash, group_id, vk_implicit_flow_token, api_version)

    download_xkcd_comic()
    publicate_comic(vk_implicit_flow_token,  group_id, api_version,  owner_id, photo_id)


if __name__ == "__main__":
    main()