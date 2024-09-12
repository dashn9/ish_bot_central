import json
import requests
from pymongo import MongoClient
from flask import current_app
from flaskr.models.identity import BotIdentityModel


class IdentityService:
    __db_client = None

    def __init__(self, db_client: MongoClient) -> None:
        self.__db_client = db_client

    def resolve_smartproxy_url(self, proxy_geo, session_duration="5"):
        return f"user-<smartproxy_user>-{proxy_geo}-{session_duration and '-session-duration-'+session_duration}:<smartproxy_password>@{current_app.config['SMARTPROXY_HOST']}:{current_app.config['SMARTPROXY_PORT']}"

    def get_identity(self, method: str, value: dict | str | int = None) -> dict:
        identity = {}
        if method == "id":
            identity = BotIdentityModel(self.__db_client).fetch_identity_by_id(value)
        elif method == "random":
            identity = BotIdentityModel(self.__db_client).fetch_random_identity()

        identity.pop("_id")
        try:
            identity["TIMEZONE"].pop("full_info")
        except KeyError:
            pass
        identity["PROXY_URL"] = self.resolve_smartproxy_url(identity["PROXY_GEO"])

        return identity

    @staticmethod
    def timezone_ip_timezone_api_url_resolver(timezone_id):
        url = f"http://worldtimeapi.org/api/timezone/{timezone_id}"
        return url

    def update_timezone(self, identity_id, timezone: dict) -> bool:
        identity = BotIdentityModel(self.__db_client)
        identity.fetch_identity_by_id(identity_id)
        identity.update_timezone_details(timezone)
        return True

    def update_cookies(self, identity_id, cookies: list) -> bool:
        identity = BotIdentityModel(self.__db_client)
        identity.fetch_identity_by_id(identity_id)
        identity.update_cookies(cookies)
        return True

    def get_timezone(self, ip_addr: str, identity_id: int = None) -> dict:
        with open("./flaskr/files/timezones_abbr_map.json") as f:
            timezone_fulls = json.load(f)
        fetched_timezone = {
            "id": None,
            "full_name": None,
            "offset": None,
            "full_info": {},
        }
        ipapi_response = requests.get(
            f"http://ip-api.com/json/{ip_addr}?fields=53137215"
        ).json()

        worldtimeapi_response = requests.get(
            self.timezone_ip_timezone_api_url_resolver(ipapi_response["timezone"])
        ).json()

        fetched_timezone["full_name"] = timezone_fulls.get(
            worldtimeapi_response["abbreviation"], None
        )

        fetched_timezone["id"] = ipapi_response["timezone"]
        fetched_timezone["offset"] = round(ipapi_response["offset"] / 60)
        fetched_timezone["full_info"] = ipapi_response

        if identity_id:
            self.update_timezone(identity_id, fetched_timezone)

        return fetched_timezone
