from fastapi import FastAPI, APIRouter
from routers.users import users_router

app = FastAPI()

routers = [users_router]

for router in routers:
    app.include_router(users_router)