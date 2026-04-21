
from datetime import datetime, timedelta
from database.database import users_collection
from auth.genrateotp import generate_otp


async def resend_otp(email):
    user = await users_collection.find_one({"email": email})

    if not user:
        return False, "User not found"

    otp = generate_otp()

    await users_collection.update_one(
        {"email": email},
        {"$set": {
            "otp": otp,
            "otp_expiry": datetime.utcnow() + timedelta(minutes=5)
        }}
    )

    return True, otp