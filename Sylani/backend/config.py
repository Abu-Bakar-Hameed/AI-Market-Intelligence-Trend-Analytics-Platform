from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")






JWT_SECRET = os.getenv("JWT_SECRET")
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY", JWT_SECRET)  # fallback if missing
RESET_SECRET_KEY = os.getenv("RESET_SECRET_KEY", JWT_SECRET)    # fallback if missing
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Convert minutes to int and provide defaults
ACCESS_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
RESET_EXPIRE_MINUTES = int(os.getenv("RESET_EXPIRE_MINUTES", 15))  # make sure this is in your .env

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")