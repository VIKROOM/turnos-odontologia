import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlsplit, urlunsplit
from uuid import uuid4

import psycopg
import pytest

from app.config import get_settings


@pytest.fixture(scope="session")
def database_url() -> str:
    """URL de la base para tests: siempre el servicio `db` (postgres:15-alpine).

    Fuera de Docker el nombre de servicio `db` no resuelve en el host y el
    puerto publicado puede no ser 5432 (conflicto con otro PostgreSQL del host);
    se reconstruye hacia localhost usando el puerto de exposición (DB_PORT).
    Dentro de Docker (IN_DOCKER=1) se usa el nombre de servicio tal cual.
    """
    settings = get_settings()
    url = settings.database_url
    if "IN_DOCKER" in os.environ:
        return url
    parts = urlsplit(url)
    auth = ""
    if parts.username:
        auth = parts.username
        if parts.password:
            auth += f":{parts.password}"
        auth += "@"
    netloc = f"{auth}localhost:{settings.db_port}"
    return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))


@pytest.fixture(scope="session")
def migrated_database(database_url: str) -> str:
    """Aplica `alembic upgrade head` contra la db real antes de los tests.

    Sin revisiones creadas, `alembic upgrade head` es un no-op y los tests
    fallan con `relation ... does not exist` (RED legítimo). Una vez que la
    migración existe, aplica el esquema. El override de `DATABASE_URL` (que
    gana sobre el `.env`) hace que `env.py` use la db del compose desde el host.
    """
    backend_dir = Path(__file__).resolve().parent.parent
    env = os.environ.copy()
    env["DATABASE_URL"] = database_url
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(backend_dir),
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(
            "alembic upgrade head falló:\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return database_url


@pytest.fixture
def db(migrated_database: str):
    """Conexión psycopg a PostgreSQL real, aislada por rollback al terminar.

    Cada test corre dentro de una transacción que se revierte en el teardown, de
    modo que no colisiona con otros tests ni deja datos de negocio. Los inserts
    que se espera que violen una restricción se envuelven en un SAVEPOINT
    (`conn.transaction()` anidado) para poder continuar tras el error.
    """
    conn = psycopg.connect(migrated_database, autocommit=False)
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()


@pytest.fixture
def api_env(database_url: str, monkeypatch: pytest.MonkeyPatch) -> str:
    """DATABASE_URL del proceso -> base del compose en el host (mismo override que C-02).

    Desde el host el nombre de servicio `db` no resuelve; se fuerza la URL a
    `localhost:<DB_PORT>` y se limpia la caché de settings para que las
    conexiones por-request del API apunten a postgres:15-alpine del compose.
    """
    monkeypatch.setenv("DATABASE_URL", database_url)
    get_settings.cache_clear()
    yield database_url
    get_settings.cache_clear()


@pytest.fixture
def client(api_env: str):
    """Cliente HTTP contra la app FastAPI real (sin lifespan: el router conecta por request).

    `raise_server_exceptions=False` para ver el código HTTP real cuando un
    error escapa sin mapear (p. ej. 500 antes de implementar D4).
    """
    from fastapi.testclient import TestClient

    from app.main import app

    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def agenda_seed(migrated_database: str):
    """Filas base COMITEADAS para tests de API: 2 recursos, paciente, prácticas 10/30/60.

    A diferencia de `db` (aislado por rollback), el API escribe desde su propia
    conexión: las FK deben estar commiteadas para que los INSERT del caso de uso
    las vean. El teardown elimina todo para que la suite sea repetible.
    """
    conn = psycopg.connect(migrated_database, autocommit=True)
    sufijo = uuid4().hex[:8]

    def insertar(sql: str, params: tuple):
        return conn.execute(sql, params).fetchone()[0]

    recurso1 = insertar("INSERT INTO recurso (nombre) VALUES (%s) RETURNING id", (f"Sillon A {sufijo}",))
    recurso2 = insertar("INSERT INTO recurso (nombre) VALUES (%s) RETURNING id", (f"Sillon B {sufijo}",))
    paciente = insertar(
        "INSERT INTO paciente (nombre, telefono) VALUES (%s, %s) RETURNING id",
        (f"Paciente {sufijo}", f"+5411{sufijo}01"),
    )
    practica10 = insertar(
        "INSERT INTO practica (nombre, duracion_minutos) VALUES (%s, 10) RETURNING id",
        (f"Revision 10m {sufijo}",),
    )
    practica30 = insertar(
        "INSERT INTO practica (nombre, duracion_minutos) VALUES (%s, 30) RETURNING id",
        (f"Consulta 30m {sufijo}",),
    )
    practica60 = insertar(
        "INSERT INTO practica (nombre, duracion_minutos) VALUES (%s, 60) RETURNING id",
        (f"Ortodoncia 60m {sufijo}",),
    )

    yield SimpleNamespace(
        recurso1=recurso1,
        recurso2=recurso2,
        paciente=paciente,
        practica10=practica10,
        practica30=practica30,
        practica60=practica60,
        conn=conn,
    )

    conn.execute("DELETE FROM reserva_agenda WHERE recurso_id IN (%s, %s)", (recurso1, recurso2))
    conn.execute("DELETE FROM practicaduracion WHERE recurso_id IN (%s, %s)", (recurso1, recurso2))
    conn.execute("DELETE FROM practica WHERE id IN (%s, %s, %s)", (practica10, practica30, practica60))
    conn.execute("DELETE FROM paciente WHERE id = %s", (paciente,))
    conn.execute("DELETE FROM recurso WHERE id IN (%s, %s)", (recurso1, recurso2))
    conn.close()
