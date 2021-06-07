from telethon.sync import TelegramClient, events
from telethon.tl.custom import Button
from constants.districts import districts
from db import getSubscriberCount
from main import pollingCore
import sys


from conversations.conversation import userSubscritionStatus,startCheckAvailabilityConversion,startRuleSelectionConversation,startSubscriptionConversation
from lib.keyboard import KeyBoardOptions
import auth.telegram as TELEGRAM_CREDS
import lib.messages as MESSAGES
from lib.utils import validatePincode
keyBoardOptions = KeyBoardOptions()

distViewKeyboard = keyBoardOptions.distViewKeyboard
distSubscribeKeyboard = keyBoardOptions.distSubscribeKeyboard
mainKeyboard = keyBoardOptions.mainKeyboard


bot = TelegramClient('bot', TELEGRAM_CREDS.api_id,TELEGRAM_CREDS.api_hash).start(bot_token=TELEGRAM_CREDS.bot_token)




@bot.on(events.NewMessage(func=lambda e: e.is_private))
async def handler(event):
    sender = await event.get_sender()
    message = event.raw_text
    if message == keyBoardOptions.checkAvailability:
        try:

            await startCheckAvailabilityConversion(bot,event)
        except:
            await bot.send_message(sender.id,MESSAGES.conversationTimedout)
            await bot.send_message(sender.id,MESSAGES.helloMessage,buttons=mainKeyboard)

        return
    elif message==keyBoardOptions.backButton:
        await bot.send_message(sender.id,MESSAGES.helloMessage,buttons=mainKeyboard)
        return

     
    elif message == keyBoardOptions.subscribeToAlerts:
        # await bot.send_message(sender.id, "🌎 Subscribe to ALerts ", buttons=keyBoardOptions.subscribtionButtons)
        try:
            await startSubscriptionConversation(bot,event)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            await bot.send_message(sender.id,MESSAGES.conversationTimedout)
            await bot.send_message(sender.id,MESSAGES.helloMessage,buttons=mainKeyboard)
        return
    elif message == keyBoardOptions.subscribtion:
        status = await userSubscritionStatus(sender.id)
        if status:
            await bot.send_message(sender.id, MESSAGES.subscribedTo+status)
            await bot.send_message(sender.id, MESSAGES.bookedConfirmation, buttons=[Button.inline(MESSAGES.unsubscribeNow, "unsubscribe")])
        else:
            await bot.send_message(sender.id, MESSAGES.noActiveSubscription)
        return
    elif message == keyBoardOptions.howToBook:
        await bot.send_message(sender.id, MESSAGES.howToBook)
        return
    elif message == keyBoardOptions.helpFaq:
        await bot.send_message(sender.id, MESSAGES.helpAndFaq)
        return
    elif message == keyBoardOptions.about:
        await bot.send_message(sender.id,MESSAGES.buildAboutBotMessage(await getSubscriberCount()))
        return

    elif message == "/start":
        print("Star")
        await bot.send_message(sender.id, MESSAGES.helloMessage, buttons=mainKeyboard)
        return



@bot.on(events.NewMessage(incoming=True, pattern='intialise'))
async def handlerPoll(event):
    await pollingCore(bot)
    sender = await event.get_sender()
    bot.send_message(sender.id, "Core intialised")




bot.run_until_disconnected()
