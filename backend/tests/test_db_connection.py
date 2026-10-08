from sqlalchemy import create_engine, text


def test_db_connection_against_postgres_service(database_url: str) -> None:
    engine = create_engine(database_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
    engine.dispose()
