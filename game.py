import requests
import time
import json


class nCoV:
    VK_API_ENDPOINT = "https://api.vk.com/method/"
    GAME_API_ENDPOINT = "https://ncov.w83.vkforms.ru/api/"

    def __init__(self, access_token: str, friends_access_token: str = None):
        self.access_token = access_token
        if friends_access_token is None:
            friends_access_token = self.access_token

        self.session = requests.Session()
        response = self.session.get(
            self.VK_API_ENDPOINT + "apps.get",
            params={"access_token": self.access_token, "app_id": 7301988, "v": 5.109},
        ).json()["response"]

        self.webview_url = response["items"][0]["webview_url"]
        self.session.headers["X-Vk-Sign"] = self.webview_url.split("?")[1]

        print(self.webview_url)
        print()

        self.friends_list = self.session.get(
            self.VK_API_ENDPOINT + "friends.get",
            params={
                "access_token": friends_access_token,
                "count": 1000000,
                "v": 5.109,
                "user_id": 578560240,
            },
        ).json()["response"]["items"]

    def _game_api_request(self, method: str, **kwagrs):
        response = self.session.post(self.GAME_API_ENDPOINT + method, **kwagrs)
        try:
            return response.json()["response"]
        except json.JSONDecodeError:
            print(response.text)
            time.sleep(1)
            return self._game_api_request(method, **kwagrs)

    def index(self):
        return self._game_api_request("index", data={})

    def government_take(self):
        return self._game_api_request("government/take", data={})

    def government_steal(self, steal_from: int):
        return self._game_api_request(
            "government/steal", data={"steal_from": steal_from}
        )

    def eat(self):
        return self._game_api_request("eat", data={})

    def top(self, top_type="all"):
        return self._game_api_request(
            "top/" + top_type,
            data={"list": self.friends_list} if top_type == "friends" else {},
        )

    def item_transfer(self, transfer_to: int):
        return self._game_api_request(
            "item/transfer", data={"transfer_to": transfer_to}
        )
