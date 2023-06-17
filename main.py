import os
import re
import requests
from dotenv import load_dotenv

API_URL = "https://api-ssl.bitly.com/v4/"


def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    user_input = input("Введите ссылку, которую хотите сократить, \n"
                       "или битлинк, для которого хотите узнать количество переходов: ").strip()

    if is_bitlink(TOKEN, user_input):
        try:
            count = get_clicks_count(TOKEN, user_input)
            print("Переходов по ссылке:", count)
        except requests.exceptions.HTTPError as e:
            print("Введена некорректная ссылка. Код ошибки", str(e)[:3])
            os.system("pause")
    else:
        title = input("Введите название для ссылки (не обязательно): ")
        try:
            bitlink = shorten_link(TOKEN, user_input, title)
            print("Битлинк " + bitlink)
        except requests.exceptions.HTTPError as e:
            print("Введена некорректная ссылка. Код ошибки", str(e)[:3])
            os.system("pause")

    os.system("pause")


def shorten_link(token: str, url: str, name: str = None) -> str:
    api_method_url = API_URL + "bitlinks"

    auth_header = {
        "Authorization": f"Bearer {token}"
    }
    request_params = {
        "long_url": f"{url}",
        "name": name
    }
    bitlink_response = requests.post(
        api_method_url,
        headers=auth_header,
        json=request_params
    )
    bitlink_response.raise_for_status()

    return bitlink_response.json()['link']


def get_clicks_count(token: str, bitlink: str) -> int:
    if re.match('http', bitlink):
        bitlink = bitlink.split("//")[1]

    api_method_url = API_URL + f"bitlinks/{bitlink}/clicks/summary"

    auth_header = {
        "Authorization": f"Bearer {token}"
    }
    request_params = {

    }
    bitlink_response = requests.get(
        api_method_url,
        headers=auth_header,
        params=request_params
    )
    bitlink_response.raise_for_status()

    return bitlink_response.json()['total_clicks']


def is_bitlink(token: str, url: str):
    auth_header = {
        "Authorization": f"Bearer {token}"
    }

    if re.match('http', url):
        url = url.split("//")[1]
    bitlink_response = requests.get(API_URL + f"/bitlinks/{url}", headers=auth_header)
    if bitlink_response.ok:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
