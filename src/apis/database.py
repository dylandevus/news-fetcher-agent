from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# Get Supabase credentials from environment variables for security
# Default to SQLite if environment variables are not set
SUPABASE_PASSWORD = os.environ.get("SUPABASE_PASSWORD")
SUPABASE_HOST = os.environ.get("SUPABASE_HOST", "yckclwyjevowdcxurdhw.supabase.co")
SUPABASE_USER = os.environ.get("SUPABASE_USER", "postgres")
SUPABASE_DB = os.environ.get("SUPABASE_DB", "postgres")
SUPABASE_PORT = os.environ.get("SUPABASE_PORT", "5432")

# If password is provided, use Supabase PostgreSQL, otherwise fallback to SQLite
if SUPABASE_PASSWORD:
    # URL-encode the password to handle special characters
    encoded_password = quote_plus(SUPABASE_PASSWORD)
    SQLALCHEMY_DATABASE_URL = f"postgresql://{SUPABASE_USER}:{encoded_password}@{SUPABASE_HOST}:{SUPABASE_PORT}/{SUPABASE_DB}"
    connect_args = {}
    print(f"\n🚀 Connected to Supabase PostgreSQL database at {SUPABASE_HOST}\n")
else:
    # Fallback to SQLite for local development or when credentials are not provided
    SQLALCHEMY_DATABASE_URL = "sqlite:///./news.db"
    connect_args = {"check_same_thread": False}
    print("\n📁 Using local SQLite database: news.db\n")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
