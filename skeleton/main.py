from fastapi import FastAPI, APIRouter
from routers.users import users_router
from routers.courses import courses_router
from routers.sections import sections_router

app = FastAPI()

routers = [users_router, courses_router, sections_router]

for router in routers:
    app.include_router(router)
