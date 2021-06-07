





def filterCenters(centers,rules):
    def centerFilterProxy(center):
        return isEligibleCenter(center,rules)

    filteredCenters=filter(centerFilterProxy,centers)
    return list(filteredCenters)

def isEligibleCenter(center,rules):

    def sessionFilterProxy(session):
        return isEligibleSession(session,rules)
    if(rules["fee_type"]):
        if(center["fee_type"]!=rules["fee_type"]):
            return False
    sessions=list(filter(sessionFilterProxy,center["sessions"]))
    if(not sessions):
        return False
    return True

def isEligibleSession(session,rules):

    if(session["available_capacity"]==0):
        return False
    if(rules.get("min_age_limit")):
        if(session["min_age_limit"]!=rules["min_age_limit"]):
            return False
    if(rules.get("vaccine")):
        if(session["vaccine"]!=rules["vaccine"]):
            return False


    if(rules.get("dose")):
        dose="available_capacity_dose2" if (rules["dose"]=="D2") else "available_capacity_dose1"
        if session[dose]==0:
            return False

    return True
        




