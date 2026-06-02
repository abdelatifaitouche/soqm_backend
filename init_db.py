import asyncio
from sqlalchemy import create_engine, text
from src.core.config import settings


def create_database():
    """Create database if it doesn't exist - runs before Alembic"""

    # Parse the async URL to a sync URL for this operation
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

    # Connect to default postgres database
    default_url = sync_url.rsplit("/", 1)[0] + "/postgres"

    try:
        engine = create_engine(default_url, isolation_level="AUTOCOMMIT")

        with engine.connect() as conn:
            conn.connection.autocommit = True

            # Extract database name
            db_name = sync_url.split("/")[-1]

            # Check if exists
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            )

            if result.fetchone() is None:
                print(f"📦 Creating database '{db_name}'...")
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"✓ Database '{db_name}' created")
            else:
                print(f"✓ Database '{db_name}' already exists")

        engine.dispose()
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    success = create_database()
    exit(0 if success else 1)
