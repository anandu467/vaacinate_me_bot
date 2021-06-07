import httpx
import ujson
from constants.districts import districts
import datetime
import asyncio
from db import addSubscibtion, getSubscibtions, getSubscibtionsByPIN, pincodes
from time import sleep
from telethon.tl.custom import Button
import sys
from lib.filterCore import filterCenters
from lib.parser import parseCenterList
from lib.keyboard import KeyBoardOptions


requestsCount = 1
stateData = []
pinMap = {}

lastMessage = {}



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Origin': 'https://www.cowin.gov.in',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.cowin.gov.in/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
}


async def getCenters(districtId):
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    global headers
    params = {
        'district_id':districtId,
        'date': today,
    }
    async with httpx.AsyncClient() as requests:
        response = await requests.get(
            'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict', headers=headers, params=params)
    centers = ujson.loads(response.text)["centers"]
    centers = filter(isVaccineAvailable, list(centers))
    centers = list(centers)
    return centers


async def getFilteredCenters(districtId, rules):
    centers = await getCenters(districtId)
    eligibleCenters = filterCenters(centers, rules)
    return list(eligibleCenters)

async def getFilteredCentersByPIN(pin,rules):
    centers=await getCentersByPIN(pin)
    eligibleCenters = filterCenters(centers, rules)
    return list(eligibleCenters)


async def getCentersByPIN(pincode):
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    global headers
    params = {
        'pincode':pincode,
        'date': today,
    }
    async with httpx.AsyncClient() as requests:
        response = await requests.get(
            'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin', headers=headers, params=params)
    centers = ujson.loads(response.text)["centers"]
    centers = filter(isVaccineAvailable, list(centers))
    centers = list(centers)
    return centers


def checkCentersByPIN(pincode):

    global pinMap

    centers = pinMap.get(pincode)
    if(centers):
        return centers


def isVaccineAvailable(center):
    sessions = center["sessions"]
    return(any([session for session in sessions if session["available_capacity"] > 0]))


async def alertSubscribers(client, subscribers, results,messageTypeId):

    if(not subscribers or not results):
        return

    for subscriber in subscribers:
        try:
            rules={}
            userId = subscriber.get('userId')
            print("sending",userId)
      
            if(subscriber.get('rules')):
                rules = subscriber.get('rules')
                results = filterCenters(results, rules)
            if(not isCenterDataChanged(messageTypeId,results,rules)):
                    continue
            # print(subscriber)
            await sendMessage(client, userId, results)
        except:
            print("Unexpected error:", sys.exc_info()[0])



async def sendMessage(client, subscriber, results, unsubMessage=False):

    if(not subscriber or not results):
        return
    try:
        results = parseCenterList(results)

        for x in range(0, len(results), 5):
            message = "\n".join(results[x:x+5])

            await client.send_message(int(subscriber), message)
        await client.send_message(int(subscriber),"🌐 <a href='https://selfregistration.cowin.gov.in/'>Book Now: Cowin Portal</a>",parse_mode='html')
        if(unsubMessage):
            await client.send_message(int(subscriber), "Booked your vaccine ?? ", buttons=[Button.inline(" 🛑 Stop Alerts", "unsubscribe")])

    except:
        print("Unexpected error:", sys.exc_info()[0])


def makePinMap():
    global stateData
    global pinMap
    global pincodes
    for center in stateData:
        pincode = center["pincode"]
        if(str(pincode) not in pincodes):
            continue
        if(pinMap.get(pincode)):
            pinMap[pincode].append(center)
            continue
        pinMap[pincode] = [center]
    print(pincodes)
    stateData = []


def updateStateData(centers):
    global stateData
    stateData.extend(centers)


def isCenterDataChanged(messageTypeId, centers,rules):
    global lastMessage
    hashKey =generateHashKey(messageTypeId,rules)

    if(lastMessage.get(hashKey) == hash(str(centers))):
        print("no change"+str(messageTypeId))
        return False
        

    lastMessage[hashKey] = hash(str(centers))


    return True


def generateHashKey(messageTypeId,rules):

    
    combined =str(messageTypeId)+str(rules.values())
    return hash(combined)


async def pollingCore(client):
    global requestsCount
    global lastMessage
    global pinMap
    while True:
        for districtId in districts:
            messageRepo = []
            requestsCount += 1
            print(requestsCount)
            centers = await getCenters(districtId)
            if(centers):
                updateStateData(centers)

                try:
                    subscribers = await getSubscibtions(districtId)

                except:
                    pass
                messageRepo.append(alertSubscribers(client, subscribers, centers,districtId))
            asyncio.gather(*messageRepo)
            del centers
            del messageRepo
        makePinMap()
        for pin in pinMap.keys():
            try:
                centers = checkCentersByPIN(pin)

                subscribers = await getSubscibtionsByPIN(pin)

                await alertSubscribers(client, subscribers, centers,pin)
            except:
                pass
        pinMap.clear()
        print("cleared")
        print(lastMessage)

        await asyncio.sleep(500)
