from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.material_routes import router as material_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(material_router, prefix="/materials")