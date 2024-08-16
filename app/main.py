from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from starlette.exceptions import HTTPException
from app.src.routers.api import router as router_api
from app.src.core.database import engine, SessionLocal, Base
from app.src.core.config import API_PREFIX, ALLOWED_HOSTS

def get_app() -> FastAPI:
    ''' Configure and run FastAPI app'''
    
    app = FastAPI()
    
    ## Generate database tables
    Base.metadata.create_all(bind=engine)
    
    app.include_router(router_api, prefix=API_PREFIX)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
    return app
    
app = get_app()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    '''
    The middleware we'll add (just a function) will create
    a new SQLAlchemy SessionLocal for each request, add it to
    the request and then close it once the request is finished.
    '''
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True, workers=2)