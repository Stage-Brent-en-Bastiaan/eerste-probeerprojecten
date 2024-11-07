import requests
import configparser
from .Models2 import PatientGet, apiurl
import json
from requests.auth import HTTPBasicAuth
from pprint import pprint

# de basis url voor alle calls die met patienten te maken hebben
apiurl = apiurl + "patients?"


# api call
def getPatienten(parameters):
    returnType = PatientGet
    config = configparser.ConfigParser()
    config.read(".ini")
    user = config["api"]["username"]
    psswd = config["api"]["password"]
    url = f"{apiurl}{parameters}"
    print("-requesting: ", url)
    headers = {"Accept": "application/json"}

    response = requests.get(
        url, auth=HTTPBasicAuth(user, psswd), headers=headers, verify=False
    )
    print("-responseStatus: ", response.status_code)
    if response.status_code == 200:
        responseDict = response.json()
        # print("response json: ",responseDict)
        # print("first patient: ",responseDict[0])
        patients = []
        for patient in responseDict:
            patients.append(returnType.from_dict(patient))
        # print("python patienten:",patients)
        return patients
    else:
        # print("-fout bij request: ",response.json()["error_message"])
        # print("-error: ",response.json()["error_message"])
        raise ConnectionError(
            f"could not get patienten from request:{url} {response.reason}"
        )
        return []


# patients=apiCall("first_name=Aycan",Patient)
# teller=0
# for patient in patients:
#      print(f"-Patient {teller}:")
#      pprint(vars(patient))
#      teller=teller+1
