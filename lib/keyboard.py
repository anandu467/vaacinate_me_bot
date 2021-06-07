from telethon.tl.custom import Button
from constants.districts import districts
class KeyBoardOptions:
    def __init__(self):
        self.checkAvailability ="Check Availability";
        self.subscribeToAlerts="Subscribe to Alerts";
        self.subscribtion="Your Subscription";
        self.howToBook="How to Book";
        self.helpFaq="Help and FAQ";
        self.about="About"
        self.bookNow="Book Now"

        self.bookNowButton=Button.url(self.bookNow,"https://selfregistration.cowin.gov.in/")

        # subscribtion keyboard

        self.subscribeByPin="Get Alerts By PIN Code"
        self.subscribeByDistrict="Get Alerts By District"
        self.backButton="Back to Main Menu"


        # checkAvailability keyboard

        self.checkByPin="Check By Pin Code"
        self.checkByDistrict="Check By District Name"


        #Rule Selectiom Wizard
        #Vaccine Type

        self.covishield ="Covishield"
        self.covaxin=" Covaxin "
        self.all="  All  "

        self.ruleSelectionVaccineType=[Button.inline(self.covishield,"COVISHIELD"),Button.inline(self.covaxin,"COVAXIN"),Button.inline(self.all," ")]

        #Fee Type
        self.free="  Free  "
        self.paid="  Paid  "
        

        self.ruleSelectionFeeType=[Button.inline(self.free,"Free"),Button.inline(self.paid,"Paid"),Button.inline(self.all," ")]

        #DOse
        self.dose1=" Dose 1 "
        self.dose2=" Dose 2 "
        self.both="  Both  "

        self.ruleSelectionDoseType=[Button.inline(self.dose1,"D1"),Button.inline(self.dose2,"D2"),Button.inline(self.both," ")]

        #Age Limit

        self.eighteen="   18+   "
        self.fortyfive="   45+   "
        self.ruleSelectionAgeLimit=[Button.inline(self.eighteen,"18"),Button.inline(self.fortyfive,"45"),Button.inline(self.both,"0")]




        self.mainKeyboard=[[Button.text(self.checkAvailability,resize=True),Button.text(self.subscribeToAlerts,resize=True)],
                    [Button.text(self.subscribtion,resize=True),Button.text(self.howToBook,resize=True)],
                    [Button.text(self.helpFaq,resize=True),Button.text(self.about,resize=True)]]
        self.distViewKeyboard =self.makeGrid([Button.inline(districts[x],"check-"+x) for x in districts])
        self.distSubscribeKeyboard =self.makeGrid([Button.inline(districts[x],"subscribe-"+x) for x in districts])
        self.subscribtionButtons=[[Button.text(self.subscribeByPin,single_use=True,resize=True)],[Button.text(self.subscribeByDistrict,single_use=True,resize=True)],[Button.text(self.backButton,single_use=True,resize=True)]]
        self.checkAvailabilityButtons=[[Button.text(self.checkByPin,single_use=True,resize=True)],[Button.text(self.checkByDistrict,single_use=True,resize=True)],
        [Button.text(self.backButton,single_use=True,resize=True)]]
   

    # def buildKeyboard(self):
    #     return self.mainKeyboard
    def makeGrid(self,keyBoard):
        return [keyBoard[x:x+2] for x in range(0,len(keyBoard),2)]
