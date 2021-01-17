import os
import requests
import json


def getToken():
    # get credentials
    f = open(os.path.join("local", "resources",
                          "innovation.credentials.json"), "r")
    credentials = json.loads(f.read())
    # prepare headers
    myHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': "Bearer"
    }
    # prepare url
    myUrl = "https://login.microsoftonline.com/" + \
        credentials["tenant"] + "/oauth2/token"
    # prepare reques body
    myData = {
        "grant_type": "client_credentials",
        "client_id": credentials["appId"],
        "client_secret": credentials["password"],
        "resource": "https://management.azure.com"
    }
    # send request
    result = requests.post(myUrl, data=myData, headers=myHeaders)
    # extract token
    data = json.loads(result.text)
    return data["access_token"]
