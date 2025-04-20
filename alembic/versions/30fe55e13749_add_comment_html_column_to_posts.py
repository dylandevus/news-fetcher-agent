"""add_comment_html_column_to_posts

Revision ID: 30fe55e13749
Revises: 4202fbeac7ba
Create Date: 2025-04-19 22:24:30.837762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30fe55e13749'
down_revision = '4202fbeac7ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the comment_html column to the posts table if it doesn't already exist
    from sqlalchemy import inspect, text
    
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Check if posts table exists
    if 'posts' in inspector.get_table_names():
        # Check if the column already exists
        columns = [col['name'] for col in inspector.get_columns('posts')]
        if 'comment_html' not in columns:
            op.add_column('posts', sa.Column('comment_html', sa.Text(), nullable=True))
            print("Added comment_html column to posts table")
        else:
            print("comment_html column already exists in posts table")
    else:
        print("posts table does not exist - skipping migration")


def downgrade() -> None:
    # Remove the comment_html column if it exists
    op.drop_column('posts', 'comment_html')
