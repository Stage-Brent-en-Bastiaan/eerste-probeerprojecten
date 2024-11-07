# import os
# print("working directory:",os.getcwd())
# os.chdir(os.getcwd()+'/webui/ApiCommunication')
import requests
import configparser
from .Models2 import MessageGet, apiurl
from requests.auth import HTTPBasicAuth
from pprint import pprint
from datetime import timedelta, datetime
from Config import Config
import json
from dataclasses import asdict
from functools import reduce

# de basis url voor alle calls die met messages te maken hebben
apiurl = apiurl + "messages?"


def getMostRecentMessage():
    returnType = MessageGet
    config = configparser.ConfigParser()
    config.read(".ini")
    user = config["api"]["username"]
    psswd = config["api"]["password"]
    last_month = datetime.today() - timedelta(days=1)
    url = f"{apiurl}created_from={datetime.timestamp(last_month)}"
    print("-requesting: ", url)
    headers = {"Accept": "application/json"}

    response = requests.get(
        url, auth=HTTPBasicAuth(user, psswd), headers=headers, verify=False
    )
    print("responseStatus:", response.status_code)
    if response.status_code == 200:
        responseList = response.json()
        print(
            "lf test message: ",
            list(
                filter(
                    lambda message: message.get("title") == "test message", responseList
                )
            ),
        )
        mostRecentMessage = returnType.from_dict(
            dict(
                reduce(
                    lambda accum, new: accum
                    if accum.get("created_timestamp") > new.get("created_timestamp")
                    else new,
                    responseList,
                )
            )
        )
        print("recentste patient", mostRecentMessage)
        return mostRecentMessage
    else:
        # print(response.status_code)
        raise ConnectionError(response.json()["error_message"])
        return None


def PostNewMessage(Message):
    config = configparser.ConfigParser()
    config.read(".ini")
    user = config["api"]["username"]
    psswd = config["api"]["password"]

    url = f"{apiurl}"
    print("-posting: ", url)
    headers = {"Content-Type": "application/json;charset=utf-8"}
    messageJson = json.dumps(asdict(Message))
    print("post payload: ", messageJson)
    response = requests.post(
        url,
        auth=HTTPBasicAuth(user, psswd),
        headers=headers,
        verify=False,
        data=messageJson,
    )
    print("responseStatusCode:", response.status_code)
    print("responseStatus:", response.reason)

    if response.ok:
        print("succesvol aangemaakt")
        return response.json().get("message_id")
    else:
        print("reponsetext: ", response.text)
        # raise ConnectionError(response.json()["error_message"])
        return response.json().get("message_id")


# mostRecentMessage=getMostRecentMessage()
# print(mostRecentMessage)
