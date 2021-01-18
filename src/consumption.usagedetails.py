# https://docs.microsoft.com/en-us/rest/api/consumption/usagedetails/list

import csv
import json
import os
import requests
from sheba.arc import credentials


def saveJson(data, fileName):
    path = os.path.join("local", "data", "out", fileName + ".json")
    print("saving " + path)
    formatted = json.dumps(data, indent=4)
    f = open(path, "w")
    f.write(formatted)
    f.close()


def saveBillToCsv(data, fileName):
    path = os.path.join("local", "data", "out", fileName + ".csv")
    print("saving " + path)
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow([item, data[item]])


def getUsageDetails(subscriptionId, token, billingPeriodName):
    myUrl = "https://management.azure.com/subscriptions/" + subscriptionId
    myUrl += "/providers/Microsoft.Billing/billingPeriods/" + billingPeriodName
    myUrl += "/providers/Microsoft.Consumption/usageDetails"
    myUrl += "?api-version=2019-10-01"
    result = requests.get(myUrl, headers={
        'Content-Type': 'application/json', 'Authorization': "Bearer " + token})
    data = json.loads(result.text)
    # saveJson(data, billingPeriodName + "-usage-details")
    return data


def getSummary(subscriptionId, token, billingPeriodName):
    bill = {}
    data = getUsageDetails(subscriptionId, token, billingPeriodName)
    #saveJson(data, billingPeriodName + "-usage-details")
    for item in data["value"]:
        resourceGroup = item["properties"]["resourceGroup"].lower()
        # resourceName = item["properties"]["resourceName"]
        # date = item["properties"]["date"]
        cost = item["properties"]["cost"]
        # print(date + " " + resourceName + " " + str(cost) + " " + resourceGroup)
        if resourceGroup in bill:
            bill[resourceGroup] = bill[resourceGroup] + cost
        else:
            # print(resourceGroup)
            bill[resourceGroup] = cost
    return bill


billingPeriodName = input("Enter billing-period-name (YYYYMM): ")

if billingPeriodName is None:
    print("Argument billingPeriodName is empty")
else:
    subscriptionId = credentials.getSubscriptionId()
    token = credentials.getToken()
    bill = getSummary(subscriptionId, token, billingPeriodName)    
    saveBillToCsv(bill, billingPeriodName + "-usage-summary")
