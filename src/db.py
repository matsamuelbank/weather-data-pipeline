from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def get_database_url() -> str:
    """Build the PostgreSQL connection string from environment variables."""
    return (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


def get_engine() -> Engine:
    # On centralise la creation du moteur pour ne pas dupliquer la connexion ailleurs.
    return create_engine(get_database_url())
