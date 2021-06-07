
def validatePincode(pincode):
    pincode=str(pincode)
    return len(pincode)==6 and pincode.isdigit() and pincode[0]=="6"



