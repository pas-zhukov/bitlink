import os
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv
from argparse import ArgumentParser

API_URL = "https://api-ssl.bitly.com/v4/"


def main():
    load_dotenv()
    bily_token = os.getenv("BITLY_TOKEN")
    
    arg_parser = ArgumentParser(
        description='Программа для сокращения ссылок и подсчёта количества переходов по битлинкам.'
    )
    arg_parser.add_argument(
        'url',
        help="Ссылка для сокращения или битлинк."
    )
    args = arg_parser.parse_args()
    user_input = args.url

    if is_bitlink(bily_token, user_input):
        try:
            count = get_clicks_count(bily_token, user_input)
            print("Переходов по ссылке:", count)
        except requests.exceptions.HTTPError as e:
            print("Введена некорректная ссылка. Код ошибки",
                  e.response.status_code)
    else:
        try:
            bitlink = shorten_link(bily_token, user_input)
            print(f"Битлинк {bitlink}")
        except requests.exceptions.HTTPError as e:
            print("Введена некорректная ссылка. Код ошибки",
                  e.response.status_code)


def shorten_link(token: str, url: str, name: str = None) -> str:
    api_method_url = f"{API_URL}bitlinks"

    auth_header = {
        "Authorization": f"Bearer {token}"
    }
    request_params = {
        "long_url": url,
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
    parsed_bitlink = urlparse(bitlink)
    bitlink = f"{parsed_bitlink.netloc}{parsed_bitlink.path}"

    api_method_url = f"{API_URL}bitlinks/{bitlink}/clicks/summary"

    auth_header = {
        "Authorization": f"Bearer {token}"
    }
    bitlink_response = requests.get(
        api_method_url,
        headers=auth_header
    )
    bitlink_response.raise_for_status()

    return bitlink_response.json()['total_clicks']


def is_bitlink(token: str, url: str):
    auth_header = {
        "Authorization": f"Bearer {token}"
    }

    parsed_url = urlparse(url)
    url = f"{parsed_url.netloc}{parsed_url.path}"

    api_method_url = f"{API_URL}/bitlinks/{url}"
    bitlink_response = requests.get(api_method_url, headers=auth_header)

    return bitlink_response.ok


if __name__ == "__main__":
    main()
