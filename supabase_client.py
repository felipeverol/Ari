# supabase_client.py
from supabase import create_client
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
import os

load_dotenv()

# Cliente Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Checkpointer async para o grafo
DB_URI = os.getenv("SUPABASE_DB_URI")
pool = AsyncConnectionPool(
    DB_URI,
    max_size=10,
    open=False,
    kwargs={
        "autocommit": True,
        "options": "-c search_path=langgraph"
    }
)
checkpointer = AsyncPostgresSaver(pool)