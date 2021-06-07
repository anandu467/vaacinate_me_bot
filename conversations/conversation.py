from telethon.sync import events
from telethon.tl.custom import Button
from constants.districts import districts
from db import checkSubscription
from db import addPINSubscibtion
from main import sendMessage, getCentersByPIN, getFilteredCentersByPIN
import sys
from lib.keyboard import KeyBoardOptions
import lib.messages as MESSAGES
from lib.utils import validatePincode
keyBoardOptions = KeyBoardOptions()

distViewKeyboard = keyBoardOptions.distViewKeyboard
distSubscribeKeyboard = keyBoardOptions.distSubscribeKeyboard
mainKeyboard = keyBoardOptions.mainKeyboard


async def startRuleSelectionConversation(bot, event):
    rule = {}
    sender = await event.get_sender()
    userId = sender.id
    try:
        async with bot.conversation(await event.get_chat(), exclusive=False) as conv:
            await conv.send_message(MESSAGES.selectVaccine, buttons=keyBoardOptions.ruleSelectionVaccineType)
            resp = await conv.wait_event(press_event(userId))
            answer = str(resp.data, "UTF-8").strip()

            await resp.answer(answer+" selected" if answer else "All"+" selected")
            rule["vaccine"] = answer

            await conv.send_message(MESSAGES.selectDose, buttons=keyBoardOptions.ruleSelectionDoseType)
            resp = await conv.wait_event(press_event(userId))
            answer = str(resp.data, "UTF-8").strip()

            await resp.answer(answer+" selected" if answer else "All"+" selected")

            rule["dose"] = answer

            await conv.send_message(MESSAGES.selectFee, buttons=keyBoardOptions.ruleSelectionFeeType)
            resp = await conv.wait_event(press_event(userId))
            answer = str(resp.data, "UTF-8").strip()
            await resp.answer(answer+" selected" if answer else "All"+" selected")
            rule["fee_type"] = answer

            await conv.send_message(MESSAGES.selectAgeLimit, buttons=keyBoardOptions.ruleSelectionAgeLimit)
            resp = await conv.wait_event(press_event(userId))
            answer = str(resp.data, "UTF-8").strip()
            await resp.answer(answer+" selected" if int(answer) else "All"+" selected")
            rule["min_age_limit"] = int(answer)

            print(rule)

            conv.cancel()
            return rule
    except:
        print("Unexpected error: in conv", sys.exc_info()[0])
        await bot.send_message(sender.id, MESSAGES.conversationTimedout)
        await bot.send_message(sender.id, MESSAGES.helloMessage, buttons=mainKeyboard)


async def startSubscriptionConversation(bot, event):
    sender = await event.get_sender()
    userName = sender.username
    userId = sender.id
    async with bot.conversation(await event.get_chat()) as conv:
        msg = await conv.send_message(MESSAGES.select, buttons=keyBoardOptions.subscribtionButtons)
        resp = (await conv.get_response()).raw_text
        await msg.delete()
        print(resp)
        if resp == keyBoardOptions.subscribeByDistrict:
            await conv.send_message(MESSAGES.chooseDistrict, buttons=distSubscribeKeyboard)
            await conv.cancel_all()

            return
        elif resp == keyBoardOptions.subscribeByPin:
            currentSubscibtionStatus = await userSubscritionStatus(userId)
            if(currentSubscibtionStatus):
                await conv.send_message(MESSAGES.alreadySubscribedTo+currentSubscibtionStatus, buttons=keyBoardOptions.mainKeyboard)
                await conv.cancel_all()
                return

            await conv.send_message(MESSAGES.enterPinCode)
            pincode = (await conv.get_response()).raw_text
            while (not validatePincode(pincode)):
                await conv.send_message(MESSAGES.invalidPincode)
                pincode = (await conv.get_response()).raw_text
            print("Picode")

            rules = await startRuleSelectionConversation(bot,event)
            if(not rules):
                return
            print(rules)
            await addPINSubscibtion(userId, userName, pincode, rules)
            await conv.send_message(MESSAGES.willNotify+pincode)
            await conv.send_message(MESSAGES.subscribed, buttons=keyBoardOptions.mainKeyboard)
            currentStatus = await getFilteredCentersByPIN(pincode, rules)
            if(currentStatus):
                await sendMessage(bot, userId, currentStatus)
        # else:
        #      await conv.send_message("👋 Hello There ! \n Select an option to continue",buttons=mainKeyboard)

        await conv.cancel_all()


async def startCheckAvailabilityConversion(bot, event):
    sender = await event.get_sender()
    userName = sender.username
    userId = sender.id
    async with bot.conversation(await event.get_chat(), exclusive=True) as conv:
        msg = await conv.send_message(MESSAGES.select, buttons=keyBoardOptions.checkAvailabilityButtons)
        resp = (await conv.get_response()).raw_text
        await msg.delete()

        if resp == keyBoardOptions.checkByDistrict:
            print(resp)

            await conv.send_message(MESSAGES.chooseDistrict, buttons=distViewKeyboard)
            await conv.cancel_all()
            return
        elif resp == keyBoardOptions.checkByPin:

            await conv.send_message(MESSAGES.enterPinCode)
            pincode = (await conv.get_response()).raw_text
            while (not validatePincode(pincode)):
                await conv.send_message(MESSAGES.invalidPincode)
                pincode = (await conv.get_response()).raw_text
            currentStatus = await getCentersByPIN(pincode)
            print(currentStatus)
            if(currentStatus):
                await conv.send_message(MESSAGES.centersAvailable, buttons=keyBoardOptions.mainKeyboard)
                await sendMessage(bot, userId, currentStatus)
            else:
                await conv.send_message(MESSAGES.notAvailable+pincode)
                await conv.send_message(MESSAGES.alertConfirmation, buttons=[Button.text(MESSAGES.alertMe, single_use=True, resize=True), Button.text(MESSAGES.goBack, single_use=True, resize=True)])
                resp = (await conv.get_response()).raw_text
                if "Alert" in resp:
                    currentSubscibtionStatus = await userSubscritionStatus(userId)
                    if(currentSubscibtionStatus):
                        await conv.send_message(MESSAGES.alreadySubscribedTo+currentSubscibtionStatus, buttons=keyBoardOptions.mainKeyboard)
                        await conv.cancel_all()
                        return

                    rules = await startRuleSelectionConversation(event)
                    if(not rules):
                        return
                    print(rules)
                    await addPINSubscibtion(userId, userName, pincode, rules)
                    await conv.send_message(MESSAGES.willNotify+pincode)
                    await conv.send_message(MESSAGES.subscribed, buttons=keyBoardOptions.mainKeyboard)
                else:
                    await conv.send_message(MESSAGES.helloMessage, buttons=mainKeyboard)

        await conv.cancel_all()


async def userSubscritionStatus(userId):
    status = str(await checkSubscription(userId))
    if(len(status) == 3):
        return districts[status]
    if (len(status) == 6):
        return "pincode "+status


def press_event(user_id):
    return events.CallbackQuery(func=lambda e: e.sender_id == user_id)
