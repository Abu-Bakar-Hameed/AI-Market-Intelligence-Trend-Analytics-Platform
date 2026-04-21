from datetime import datetime
from database.database import users_collection

async def verify_user(email, otp):
    user = await users_collection.find_one({"email": email})

    if not user:
        return False, "User not found"

    if user.get("otp") != otp:
        return False, "Invalid OTP"

    if datetime.utcnow() > user.get("otp_expiry"):
        return False, "OTP expired"

    await users_collection.update_one(
        {"email": email},
        {"$set": {"is_verified": True},
         "$unset": {"otp": "", "otp_expiry": ""}}
    )

    return True, "Account verified"
