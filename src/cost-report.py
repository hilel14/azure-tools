# https://docs.microsoft.com/en-us/rest/api/cost-management/query/usage#billingaccountquery-modern


import csv
import json
import os
import requests
from sheba.arc import credentials


def loadBody(fileName):
    # Read request body from json file
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, "resources", fileName + ".json")
    f = open(path, "r")
    s = f.read()
    f.close()
    return json.loads(s)


def getData(subscriptionId, token, body):
    myHeaders = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + token
    }
    # send httpd request
    myBody = json.dumps(body)
    myUrl = "https://management.azure.com"
    myUrl += "/subscriptions/" + subscriptionId
    myUrl += "/providers/Microsoft.CostManagement/query"
    myUrl += "?api-version=2019-11-01"
    result = requests.post(myUrl, data=myBody, headers=myHeaders)
    result = json.loads(result.text)
    return result


def saveJson(data, fileName):
    path = os.path.join("local", "data", "out", fileName + ".json")
    print("saving " + path)
    formatted = json.dumps(data, indent=4)
    f = open(path, "w")
    f.write(formatted)
    f.close()


def saveCsv(rows, fileName):
    path = os.path.join("local", "data", "out", fileName + ".csv")
    print("saving " + path)
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow(row)


subscriptionId = credentials.getSubscriptionId()
token = credentials.getToken()
body = loadBody("SubscriptionQueryGrouping-Legacy")
result = getData(subscriptionId, token, body)
# saveJson(result, "cost-report")
saveCsv(result["properties"]["rows"], "cost-report")
