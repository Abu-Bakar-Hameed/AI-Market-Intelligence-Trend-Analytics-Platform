from datetime import datetime, timedelta
from database.database import users_collection
from auth.genrateotp import generate_otp
from auth.password import hash_password

async def create_user(email, password):
    otp = generate_otp()

    await users_collection.insert_one({
        "email": email,
        "password": hash_password(password),
        "is_verified": False,
        "otp": otp,
        "otp_expiry": datetime.utcnow() + timedelta(minutes=5)
    })

    return otp