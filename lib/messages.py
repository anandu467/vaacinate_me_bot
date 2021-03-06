alreadySubscribedTo ="π You are already subscribed to "
alreadySubscribed="π Already subscribed."
selected=" selected."
willNotify="β We will notify you when vaccine slots are available in "
subscribed="Subscribed to alerts"
checking="π Checking available slots"
centersAvailable="Centers Available"
notAvailable="βCurrently there are no vaccine slots available in "
alertConfirmation="π Do you want receive an alert when vaccine slots are available?"
alertMe="π Alert me"
unsubscribed="Unsubscribed"
unsubscribedSuccess="π Sucessfuly unsubscribed from vaccine alerts."
selectVaccine="π   Select Vaccine "
selectDose="1οΈβ£   Select Dose "
selectFee="π΅   Select Fee Type "
selectAgeLimit="β³   Select Age Limit "
select="Select an option"
chooseDistrict="π Choose your district "
enterPinCode="Enter Your Pincode"
invalidPincode="Invaild Pin\nPlease enter a valid Kerala Pincode"

goBack="π Back"
conversationTimedout="πΈ Conversation timed out"
subscribedTo="You are subscribed to "
bookedConfirmation="Booked your slots ? "
noActiveSubscription="π You dont have any active subscriptions."
unsubscribeNow=" π Unsubscribe Now"


helloMessage='''π Hello There !
Select an option to continue.
'''


howToBook ="You can log into the Co-WIN portal using the link www.cowin.gov.in and click on the βRegister/Sign In yourselfβ tab to register for COVID-19 vaccination.Alternatively, you can also register for vaccination through the Aarogya Setu App. \n\nYou can book appointment for vaccination through Co-WIN portal after logging-in to the Co-WIN Portal through your registered mobile number. The system will show vaccination centers that allow vaccination as per the age of the citizen entered in the registration portal."
helpAndFaq='''

πββοΈ Help

Check Availability : Get the list of centers with available slots.
Subscribe to Alerts  : Get alerts when vaccine slots becomes available.
Your Subscription : View / Unsubsribe your subscription.
How to Book : Guide on the booking process.
Help and Faq : Help on different topics about the bot.
About : About the Bot.

β FAQ

1. Is the service free?

The bot is 100% free to use.

2.Where do you get the vaccine slots information?

We use the API Setu's Co-WIN Public API(same used by the official CoWin website) to collect data about the available vaccination centers.

3.So,how does it work?

We regularly check for the available vaccination centers from the above API.When there are centers available,we notify the bot users based on the subscription type.

4.Is there a chance that the bot miss a center update?

Currently we sync the data from the API every 8 minutes.There is a possibility that the bot may miss a center update that comes and disappears in this time range,though the chances are low.
'''
def buildAboutBotMessage(userCount):
    return "Vaccinate Me Bot\n---------------\n Username: @vaccinate_me_kerala_bot\n Version : 0.9 \n Creator : @dreamhacker\n Users : "+userCount+" \n\n Noticed any bugs or have some suggestions??DM me at @dreamhacker or mail me at anandumohan.pv@gmail.com"
