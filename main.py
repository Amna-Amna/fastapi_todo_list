from fastapi import FastAPI, HTTPException
from starlette import status
from .routers import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health_check", status_code=status.HTTP_200_OK)
def health_check():
    service_healthy = True
    if service_healthy:
        return {"status": "healthy"}
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable")