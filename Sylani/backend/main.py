


from fastapi import FastAPI
from router.router import router

from router.router1 import router as auth_router


app = FastAPI(title="AI-Powered Market Intelligence & Trend Analytics Platform")
app.include_router(auth_router)
app.include_router(router)
