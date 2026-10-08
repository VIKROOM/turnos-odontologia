from contextlib import contextmanager

import psycopg

from app.config import get_settings


@contextmanager
def transaccion():
    """Conexión por-request a postgres: commit si termina bien, rollback si no.

    La URL se resuelve en el momento (settings en caché), de modo que el
    override `DATABASE_URL` de los tests llegue al handler.
    """
    conn = psycopg.connect(get_settings().database_url, autocommit=False)
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()
