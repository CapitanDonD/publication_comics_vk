import requests


def download_picture(filepath, url):
    response = requests.get(url)
    image_url = response.json()['img']
    comment = response.json()['alt']
    image_response = requests.get(image_url)


    response.raise_for_status()

    with open(filepath, "wb") as file:
        file.write(image_response.content)

    return comment


if __name__ == "__main__":
    file_name = 'image.png'
    url = 'https://xkcd.com/353/info.0.json'

    print(download_picture(
        file_name,
        url,
    ))