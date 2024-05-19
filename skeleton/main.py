from fastapi import FastAPI, APIRouter
from routers.users import users_router
from routers.courses import courses_router

app = FastAPI()

routers = [users_router, courses_router]

for router in routers:
    app.include_router(router)
