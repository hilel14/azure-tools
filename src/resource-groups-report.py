import os
import requests
import json
import csv
from sheba.arc import credentials


def getResourceGroups(token, subscriptionId):
    # Build url
    myUrl = "https://management.azure.com/subscriptions/" + \
        subscriptionId+"/resourcegroups?api-version=2020-06-01"
    # prepare headers
    myHeaders = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + token
    }
    # send request
    result = requests.get(myUrl, headers=myHeaders)
    data = json.loads(result.text)
    return data


def saveToCsv(data):
    path = os.path.join("local", "data", "out", "resource-groups-report.csv")
    with open(path, mode='w', newline='\n', encoding='utf-8') as outFile:
        # writer = csv.writer(outFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(outFile)
        writer.writerow(["group", "application"])
        for group in data["value"]:
            name = group["name"]
            description = "?"
            if "tags" in group:
                tags = group["tags"]
                if "Application" in tags:
                    description = tags["Application"]
            writer.writerow([name, description])


token = credentials.getToken()
subscriptionId = credentials.getSubscriptionId()
data = getResourceGroups(token, subscriptionId)
saveToCsv(data)
