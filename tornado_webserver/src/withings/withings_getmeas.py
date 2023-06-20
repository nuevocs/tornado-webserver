from src import log
import json
import time
import datetime
import httpx
from src.withings import data_schema
from src.constant import WITHINGS_CLIENT_ID, WITHINGS_CLIENT_SECRET
import os

"""
withings api functions:
- open a config json file
- check if it is expired
- if expired, refresh the token
- if not expired, return the token
- if no token, return None
"""

client_id = WITHINGS_CLIENT_ID
client_secret = WITHINGS_CLIENT_SECRET

oath2_url = "https://wbsapi.withings.net/v2/oauth2"

logging = log.logging_func("withings-api", log.logging.INFO)
logging.debug("A script starts...")


class WithingsApi:
    def __init__(self, config_path: str) -> None:
        self.path = config_path
        self.access_token = None

    def open_config(self) -> json:
        with open(self.path) as json_file:
            tokens = json.load(json_file)
        return tokens

    def check_token(self) -> None:
        logging.debug("checking token...")
        tokens = self.open_config()
        expires_in = tokens["body"]["expires_in"]
        retrieved_datetime = tokens["body"]["retrieved_datetime"]
        refresh_token = tokens["body"]["refresh_token"]
        current_time = int(time.time())
        expected_expired = retrieved_datetime + expires_in
        logging.debug(f"expected_expired: {expected_expired}")
        logging.debug(f"now_epoch: {current_time}")
        logging.debug(f"expected_expired - now_epoch: it should be 3 hours / 10800 se\
                      c{expected_expired - current_time}")
        if expected_expired < current_time:
            logging.info("refreshing token...")
            self.refresh_token(refresh_token, refresh_token)
        else:
            self.access_token = tokens["body"]["access_token"]
            logging.info(f"valid access_token: {self.access_token}")
            return self.access_token

    def refresh_token(self, refresh_token: str, expired_access_token: str) -> None:
        headers = {
            "Authorization": f"Bearer {expired_access_token}"
        }
        refresh_token_data = {
            "action": "requesttoken",
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        refresh_token_post = httpx.post(
            url=oath2_url,
            data=refresh_token_data,
            headers=headers
        )
        if refresh_token_post.status_code == 200:
            refreshed_tokens = refresh_token_post.json()
            refreshed_tokens["body"]["retrieved_datetime"] = int(time.time())
            logging.info("refresh token success")
            logging.debug(refreshed_tokens)
            with open(self.path, 'w') as f:
                json.dump(refreshed_tokens, f)
            self.access_token = refreshed_tokens["body"]["access_token"]
            logging.info(f"new access_token: {self.access_token}")
            return self.access_token
        else:
            logging.info("refresh token failed")

    def get_token(self) -> None:
        pass


class WithingsMeasure:
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    def get_measure(self,
                    action: str,
                    meastype: str,
                    category: int,
                    startdate: int,
                    enddate: int) -> json:
        r = httpx.post(
            url="https://wbsapi.withings.net/measure",
            data={
                'action': action,
                'meastype': meastype,
                'category': category,
                'startdate': startdate,
                'enddate': enddate
                # 'lastupdate': 1686254520
            },
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        if r.status_code == 200:
            logging.debug(r.json())
            r = r.json()
            measured_response = r["body"]["measuregrps"]
            logging.info(f"You have received {len(measured_response)} items.")

            lst = []

            for data in measured_response:
                date = data["date"]
                category_id = data["category"]
                device_id = data["deviceid"]
                grpid = data["grpid"]

                for v in data["measures"]:
                    meas_data = data_schema.MeasData(
                        grpid=grpid,
                        date=date,
                        category_id=category_id,
                        device_id=device_id,
                        type=v["type"],
                        value=v["value"] * (10 ** v["unit"]),
                        key=f"{grpid}{device_id[:5]}{v['type']}"
                    )
                    lst.append(meas_data)
                    logging.info(f"measure data -   {meas_data}")


