from fastapi import FastAPI
from routers.categories import categories_router
from routers.messages import messages_router
from routers.replies import replies_router
from routers.topics import topics_router
from routers.users import users_router


routers = [
    categories_router,
    messages_router,
    replies_router,
    topics_router,
    users_router
]

app = FastAPI()

for router in routers:
    app.include_router(router)
