def parseCenterList(centers):
    districtCenterMessage = []
    for center in centers:
        centerInfo=parseCenterInfo(center);
        if(centerInfo!=None):
            districtCenterMessage.append(centerInfo)
    return districtCenterMessage

def parseCenterInfo(center):
    sessionsInfo =parseSessions(center["sessions"]);
    if(sessionsInfo):
        centerName = center["name"];
        centerId = center["center_id"];
        centerAddress = center["address"];
        centerDistrict = center["district_name"];
        feeType = center["fee_type"];
        centerMessage=f'\n🏥 Center :{centerName}\n🗺 Address : {centerAddress}\n{centerDistrict}\n💴 Fee Type : {feeType}\n';
        for session in sessionsInfo:
            centerMessage+=session;
        return centerMessage;
def parseSessions(sessions):

    validSessions =[]
    for session in sessions:
    
        if(int(session["available_capacity"])>0):

            vaccineDate = session["date"];
            vaccineName = session["vaccine"];
            vaccineCapacity = session["available_capacity"]
            ageLimit =session["min_age_limit"]
            dose1=session["available_capacity_dose1"]
            dose2=session["available_capacity_dose2"]
            vaccineMessage = f'📆 Date: {vaccineDate}  Age limit : {ageLimit}+  \n💉 Vaccine Name : {vaccineName}\n🙋‍♂️Available: D1 : {dose1} | Total : {vaccineCapacity} | D2 : {dose2}\n'
            validSessions.append(vaccineMessage);
    return validSessions;


