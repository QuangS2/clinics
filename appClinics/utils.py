def jsonUser(user):
    return {
        "name":user.name,
        "birthday":user.birthday.year,
        "gender":user.gender.name,
        "address":user.address,
        "CCCD":user.CCCD,
        "phone":user.phone
    }