import os
import time
import uuid
import requests
from requests import Response
from selenium import webdriver
from selenium.webdriver.common.by import By


def down_image(image_url: str):

    img_name: str = uuid.uuid4().hex

    with open('data/parsed_avatars.txt', 'a') as parsed_log_file:
        try:
            req: Response = requests.get(image_url[:-24] + '10000')
            if req.status_code == 200:
                with open(f'data/{img_name}.jpg', 'wb') as file:
                    file.write(req.content)

                parsed_log_file.write(f'{img_name}.jpg \t {image_url[:-24] + "10000"}\n')
            else:
                raise Exception
        except Exception:
            if os.path.exists(f'data/{img_name}.jpg'):
                os.remove(f'data/{img_name}.jpg')
            parsed_log_file.write(f'{img_name}.jpg ERROR \t {image_url[:-24] + "10000"}\n')


def parse_avatars_urls(video_url: str, max_cmt_count: int) -> list:
    avatars_urls: list = []

    # Open a YouTube page and wait some time
    driver: webdriver.Firefox = webdriver.Firefox()
    driver.get(video_url)

    time.sleep(3)

    # We are constantly writing the page until the maximum number of comments is published, or when they run out
    comment_count: int = 0
    last_avatars_len: int = 0
    used_avatars_y: list = []
    while True:
        driver.execute_script('window.scrollTo(0, window.scrollMaxY);')
        time.sleep(3)

        if comment_count == max_cmt_count - 1:
            break

        avatars_elements: list = driver.find_elements(By.TAG_NAME, 'img')

        if last_avatars_len == len(avatars_elements):
            break

        last_avatars_len = len(avatars_elements)

        for avatar_element in avatars_elements:
            if avatar_element.location['y'] not in used_avatars_y:
                driver.execute_script(f'window.scrollTo(0, {avatar_element.location["y"]});')
                time.sleep(0.1)
                avatar_src: str | None = avatar_element.get_attribute('src')

                if isinstance(avatar_src, str):
                    if avatar_src[:22] == 'https://yt3.ggpht.com/':
                        if avatar_src:
                            avatars_urls.append(avatar_src)

            comment_count += 1
            used_avatars_y.append(avatar_element.location['y'])
            if comment_count == max_cmt_count - 1:
                break

    driver.close()
    return avatars_urls


if __name__ == '__main__':
    youtube_video_url: str = input('YouTube video link: ')
    max_comment_count: int = int(input('Max comment count: '))

    avatars_urls: list = parse_avatars_urls(youtube_video_url, max_comment_count)

    with open('data/parsed_avatars.txt', 'w') as parsed_log_file:
        parsed_log_file.write(f'Parsed url: {youtube_video_url}\n'
                              f'Max comment count: {max_comment_count}\n'
                              f'Avatars count: {len(avatars_urls)}\n\n')

    for avatar_url in avatars_urls:
        down_image(avatar_url)

    print('Finish')
