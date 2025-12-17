from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.material_routes import router as material_router
from routes.school_routes import router as school_router
from routes.class_routes import router as class_router
from routes.profile_routes import router as profile_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(material_router, prefix="/materials")
app.include_router(school_router, prefix="/school")
app.include_router(class_router, prefix="/class")
app.include_router(profile_router, prefix="/profile")