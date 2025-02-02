from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Importa los modelos y la base de datos
from app.models import models  # Asegúrate de que esta ruta sea correcta
from app.database.db import Base  # El objeto Base de SQLAlchemy

# Define la URL de conexión a la base de datos
DATABASE_URL = "postgresql://postgres:19062024@localhost/ODISEA_TEST"

# Configuración de logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Configura los metadatos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        url=DATABASE_URL,  # Forzamos la URL aquí
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
