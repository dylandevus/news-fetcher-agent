# Alembic configuration file
# This file is used to configure alembic, the database migration tool

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Add the parent directory to sys.path to make src importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import Base from your models
from src.apis.models import Base
from src.apis.database import SQLALCHEMY_DATABASE_URL

# this is the Alembic Config object
config = context.config

# Setup the SQLAlchemy URL - use raw strings to avoid interpolation issues
# ConfigParser treats % as interpolation syntax, so we need to escape it
url = SQLALCHEMY_DATABASE_URL.replace('%', '%%')
config.set_main_option("sqlalchemy.url", url)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Add model's MetaData object for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
