def jsonUser(user):
    return {
        "name":user.name,
        "birthday":user.birthday.year,
        "gender":user.gender.name,
        "address":user.address,
        "CCCD":user.CCCD,
        "phone":user.phone
    }
def Prescribe(prescribe):
    return {
        "id":prescribe.id,
        "userManual": prescribe.userManual,
        "amount": prescribe.amount
    }
def Medicine(medicine):
    return {
            "id": medicine.id,
            "name": medicine.name,
            "unit":medicine.unit
    }