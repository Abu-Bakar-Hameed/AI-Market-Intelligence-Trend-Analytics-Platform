from fastapi import APIRouter, HTTPException, Depends, Body, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.database import users_collection
from schemas.models import UserSignup, VerifyOTP, ForgotPasswordSchema, ResetPasswordSchema


from service.email_service import send_otp_email, send_reset_email
from auth.create_User import create_user
from auth.verify_user import verify_user
from auth.resend_otp import resend_otp
from auth.authenticate_user import authenticate_user
from auth.jwt import create_access_token, verify_access_token, create_reset_token, verify_reset_token
from auth.password import hash_password


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ---------------- CURRENT USER ----------------
async def get_current_user(token: str = Depends(oauth2_scheme)):
    email = verify_access_token(token)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ---------------- SIGNUP ----------------
@router.post("/signup", tags=["Authentication"])
async def signup(user: UserSignup, background_tasks: BackgroundTasks):
    existing = await users_collection.find_one({"email": user.email})

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = await create_user(user.email, user.password)

    background_tasks.add_task(send_otp_email, user.email, otp)

    return {"message": "User created. OTP sent."}


# ---------------- VERIFY OTP ----------------
@router.post("/verify-otp", tags=["Authentication"])
async def verify(data: VerifyOTP):
    success, msg = await verify_user(data.email, data.otp)

    if not success:
        raise HTTPException(status_code=400, detail=msg)

    return {"message": msg}


# ---------------- RESEND OTP ----------------
@router.post("/resend-otp", tags=["Authentication"])
async def resend(email: str = Body(..., embed=True), background_tasks: BackgroundTasks = BackgroundTasks()):
    success, otp = await resend_otp(email)

    if not success:
        raise HTTPException(status_code=400, detail=otp)

    background_tasks.add_task(send_otp_email, email, otp)

    return {"message": "OTP resent"}


# ---------------- LOGIN ----------------
@router.post("/token", tags=["Authentication"])
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form.username, form.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials or not verified")

    token = create_access_token(user["email"])

    return {"access_token": token, "token_type": "bearer"}


# ---------------- PROFILE ----------------
@router.get("/profile", tags=["Authentication"])
async def profile(user=Depends(get_current_user)):
    return {
        "email": user["email"],
        "is_verified": user["is_verified"]
    }


# ---------------- FORGOT PASSWORD ----------------
# @router.post("/forgot-password", tags=["Authentication"])
# async def forgot_password(data: ForgotPasswordSchema, background_tasks: BackgroundTasks,get_current_user=Depends(get_current_user)):
#     user = await users_collection.find_one({"email": data.email})

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     token = create_reset_token(data.email)

#     background_tasks.add_task(send_reset_email, data.email, token)

#     return {"message": "Reset email sent"}


# # ---------------- RESET PASSWORD ----------------
# @router.post("/reset-password", tags=["Authentication"])
# async def reset_password(data: ResetPasswordSchema,get_current_user=Depends(get_current_user)):
#     email = verify_reset_token(data.token)

#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")

#     await users_collection.update_one(
#         {"email": email},
#         {"$set": {"password": hash_password(data.new_password)}}
#     )

#     return {"message": "Password reset successful"}

@router.post("/forgot-password", tags=["Authentication"])
async def forgot_password(
    data: ForgotPasswordSchema,
    background_tasks: BackgroundTasks
):
    try:
        user = await users_collection.find_one({"email": data.email})

        # Always return same response (security best practice)
        if user:
            token = create_reset_token(data.email)
            background_tasks.add_task(send_reset_email, data.email, token)

        return {
            "message": "If the email exists, a reset link has been sent"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post("/reset-password", tags=["Authentication"])
async def reset_password(data: ResetPasswordSchema):
    email = verify_reset_token(data.token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    await users_collection.update_one(
        {"email": email},
        {"$set": {"password": hash_password(data.new_password)}}
    )

    return {"message": "Password reset successful"}