# Database Architecture & Migrations

OSINT Agent Network uses **SQLAlchemy 2.0 (Async)** as its ORM and **Alembic** for schema migrations. By default, it runs on an asynchronous SQLite database (`aiosqlite`), but it is fully compatible with PostgreSQL (`asyncpg`) for production deployments.

## Core Models

The database schema consists of three primary tables defined in `db/models/scan.py`:

1. **`ScanTask`**: Tracks the lifecycle of an OSINT pipeline execution (pending, running, completed, failed), target information, and aggregate statistics.
2. **`IntelligenceRecord`**: Stores individual pieces of raw intelligence, the LLM analysis results, extracted IoCs/TTPs, enrichment data, and Red/Blue team validation status.
3. **`ThreatActor`**: A knowledge base of known APT groups, their aliases, origin countries, and associated MITRE ATT&CK groups.

## Initializing the Database

Before running the API server or worker, you must apply the initial database migrations:

```bash
# Run all pending migrations
alembic upgrade head
# Or using the Makefile
make db-upgrade
```

## Seeding Data

You can seed the `ThreatActor` table with well-known APT groups using the provided script:

```bash
python scripts/seed_threat_actors.py
```

## Creating New Migrations

When you modify the models in `db/models/`, you must generate a new Alembic migration script:

```bash
# Generate migration script automatically
alembic revision --autogenerate -m "Add new column to IntelligenceRecord"

# Review the generated script in alembic/versions/

# Apply the migration
alembic upgrade head
```

## Production Considerations

For production environments handling high volumes of intelligence data, SQLite is not recommended due to concurrent write locks. Switch to PostgreSQL by updating your `.env`:

```env
DATABASE_URL=postgresql+asyncpg://dbuser:dbpass@dbhost:5432/oan_db
```

Make sure to install the async driver:
```bash
pip install asyncpg
```
