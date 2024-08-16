from fastapi import APIRouter
from app.src.routers import task, user, auth
from app.src.core.config import ROUTE_PREFIX_V1

router = APIRouter()

def include_api_routes():
    ''' Include routers '''
    router.include_router(auth.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(user.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(task.router, prefix=ROUTE_PREFIX_V1)

include_api_routes()