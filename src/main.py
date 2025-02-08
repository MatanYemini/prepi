from fastapi import FastAPI
import uvicorn
from routes.call_routes import router as call_router
from routes.linkedin_routes import router as linkedin_router
from config.settings import PORT

app = FastAPI()
app.include_router(call_router)
app.include_router(linkedin_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)