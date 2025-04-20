"""add_comment_html_to_posts

Revision ID: 4202fbeac7ba
Revises: f9eff688f955
Create Date: 2025-04-19 22:19:45.404057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4202fbeac7ba'
down_revision = 'f9eff688f955'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('comment_html', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('posts', 'comment_html')
