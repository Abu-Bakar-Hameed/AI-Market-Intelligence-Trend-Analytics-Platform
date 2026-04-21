from database.database import users_collection
from auth.password import verify_password
async def authenticate_user(email, password):
    user = await users_collection.find_one({"email": email})

    if not user or not verify_password(password, user["password"]):
        return None

    if not user.get("is_verified"):
        return None

    return user