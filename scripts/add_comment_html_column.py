"""
Script to directly add the comment_html column to the posts table.
This bypasses Alembic migrations which are having issues with the migration history.
"""

from sqlalchemy import inspect, text
from src.apis.database import engine, SessionLocal
import sys

def add_comment_html_column():
    """Add comment_html column to posts table if it doesn't exist"""
    try:
        print("Connecting to database...")
        # Connect to the database
        with engine.connect() as conn:
            inspector = inspect(engine)
            
            print("Checking if posts table exists...")
            # Check if posts table exists
            tables = inspector.get_table_names()
            print(f"Found tables: {tables}")
            
            if 'posts' in tables:
                # Check if the column already exists
                columns = [col['name'] for col in inspector.get_columns('posts')]
                print(f"Current columns in posts table: {columns}")
                
                if 'comment_html' not in columns:
                    # Add the column directly with SQL
                    print("Adding comment_html column...")
                    conn.execute(text("ALTER TABLE posts ADD COLUMN comment_html TEXT"))
                    conn.commit()
                    print("✅ Successfully added comment_html column to posts table")
                else:
                    print("ℹ️ comment_html column already exists in posts table")
            else:
                print("❌ posts table does not exist in the database")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = add_comment_html_column()
    sys.exit(0 if success else 1)
