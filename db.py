import firebase_admin
from firebase_admin import db
import asyncio

loop = asyncio.get_event_loop()
cred_obj = firebase_admin.credentials.Certificate('cred.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':"https://cowinbot-6eb5e-default-rtdb.asia-southeast1.firebasedatabase.app/"
	})



pincodes=set()
registeredUsers=[]



def getPincodes():
  global pincodes
  ref=db.reference(f"/PinCode")
  pincodes=ref.get()
  pincodes= set(pincodes.keys())

getPincodes()

async def checkSubscription(userId):
    dref=db.reference("/Subs/"+str(userId))
    result=await loop.run_in_executor(None,dref.get)
    return result



async def addSubscibtion(userId,userName,districtId,rules):
  ref = db.reference("/Users/"+str(districtId))
  dref=db.reference("/Subs")
  # dref.update({userId:districtId})
  await loop.run_in_executor(None,dref.update,{userId:districtId})
  record ={userId:{
"userName":userName,
  "userId":userId,
  "rules":rules,}}
  return await loop.run_in_executor(None,ref.update,record)

async def getSubscibtions(districtId):
    ref = db.reference("/Users/"+str(districtId))
    result= await loop.run_in_executor(None,ref.get)
    if(not result):
      return
    if type(result)==dict:
      result=[x for x in result.values()]
    return result
async def stopSubscibtion(userId):
  subscription=await checkSubscription(userId)
  if(not subscription):
    return
  if(len(str(subscription))==3):
    ref = db.reference(f"/Users/{subscription}/{userId}")
  else:
    ref = db.reference(f"/PinCode/{subscription}/{userId}")
    getPincodes()
  # ref.set({})
  await loop.run_in_executor(None,ref.set,{})
  dref=db.reference(f"/Subs/{userId}")
  await loop.run_in_executor(None,dref.set,{})
  dref.set({})

  

  # By Pincode Starts




# def checkPINSubscription(userId):
#     dref=db.reference("/Subs/"+str(userId))
#     result=dref.get()
#     return result



async def addPINSubscibtion(userId,userName,pincode,rules):
  
  ref = db.reference("/PinCode/"+str(pincode))
  dref=db.reference("/Subs")
  await loop.run_in_executor(None,dref.update,{userId:pincode})
  # dref.update({userId:pincode})
  record ={userId:{
"userName":userName,
  "userId":userId,
  "rules":rules}}
  pincodes.add(pincode)
  return await loop.run_in_executor(None,ref.update,record)

async def getSubscibtionsByPIN(pincode):
    ref = db.reference("/PinCode/"+str(pincode))
    result= await loop.run_in_executor(None,ref.get)
    if(not result):
      return
    return result.values()
# def stopPINSubscibtion(userId):
#   subscription=checkPINSubscription(userId)
#   if(not subscription):
#     return

#   ref = db.reference(f"/PinCode/{subscription}/{userId}")
#   getPincodes()

#   ref.set({})
#   dref=db.reference(f"/Subs/{userId}")
#   dref.set({})

  
async def getSubscriberCount():
  dref=db.reference(f"/Subs/")
  subscriptions= await loop.run_in_executor(None,dref.get)
  return str(len(subscriptions))
  

# async def getAllSubscribers():
#   dref=db.reference(f"/Subs/")
#   subscriptions=asyncio.wait([await event_loop.run_in_executor(executor,dref.get)])
#   return list(subscriptions.keys())


# async def runInExecutorGet(dref,*params):
#   await loop.run_in_executor(None,dref.get)
