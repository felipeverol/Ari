from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.material_routes import router as material_router
from routes.school_routes import router as school_router
from routes.class_routes import router as class_router
from routes.chat_routes import router as chat_router
from routes.user_routes import router as user_router
from supabase_client import pool, checkpointer
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    await checkpointer.setup()
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth")
app.include_router(material_router, prefix="/materials")
app.include_router(school_router, prefix="/school")
app.include_router(class_router, prefix="/class")
app.include_router(user_router, prefix="/user")
app.include_router(chat_router, prefix="/chat")