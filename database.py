# database.py
import os
import ssl
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # 1. Switch standard postgresql:// prefix to asyncpg
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    # 2. Strip the query parameters that asyncpg throws errors on
    if "?" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.split("?")[0]

# 3. Create a secure SSL context for Neon since it requires TLS
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE  # Adjust to CERT_REQUIRED if you want strict validation

# 4. Initialize the async engine with connection pooling parameters for cloud hosting
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"ssl": ssl_context},
    pool_pre_ping=True,  # Crucial for serverless databases like Neon to avoid stale connections
    pool_recycle=300,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session