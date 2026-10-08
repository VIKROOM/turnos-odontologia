"""Tests de la garantía declarativa de exclusión — PostgreSQL real (D2/D5, DD-10).

Estos tests escriben DIRECTO contra `reserva_agenda`, evadiendo el dominio y
el caso de uso: prueban que la no-solapamiento la garantiza el constraint
`reserva_agenda_sin_solapamiento` (EXCLUDE USING gist), no el código de la
aplicación (RN-GEN-01). NUNCA SQLite ni dobles en memoria (DD-10).

Es autocontenido con la fixture `db` (filas creadas y revirtadas en la misma
transacción): NO se combina con `agenda_seed`, cuyo teardown haría DELETE
mientras `db` retiene filas sin commitear y bloquearía la suite.

Trazabilidad: RN-GEN-01 (garantía de exclusión declarativa en la base).
"""

from datetime import datetime, timezone

import psycopg
import pytest

UTC = timezone.utc
DIA = datetime(2026, 3, 2, tzinfo=UTC)

TURNO_INSERT_SQL = (
    "INSERT INTO reserva_agenda "
    "(tipo, estado, recurso_id, paciente_id, practica_id, inicio, fin) "
    "VALUES ('turno', 'confirmado', %s, %s, %s, %s, %s)"
)


def test_escritura_directa_solapada_rechazada_por_la_base(db):
    """RN-GEN-01 — Escenario *Escritura que evade la validación de dominio
    igualmente rechazada* (5.12 / tareas 4.1-4.2).

    Tres geometrías de solapamiento insertadas con SQL crudo, sin pasar por
    el dominio ni el caso de uso: la base responde `exclusion_violation`
    (SQLSTATE 23P01) en cada una y ninguna fila nueva queda persistida.
    """
    recurso = db.execute(
        "INSERT INTO recurso (nombre) VALUES ('Sillon EXCL') RETURNING id"
    ).fetchone()[0]
    practica = db.execute(
        "INSERT INTO practica (nombre, duracion_minutos) VALUES ('Consulta EXCL', 30) RETURNING id"
    ).fetchone()[0]
    paciente = db.execute(
        "INSERT INTO paciente (nombre, telefono) VALUES ('Ana EXCL', '+54-11-5555-0090') RETURNING id"
    ).fetchone()[0]

    db.execute(
        TURNO_INSERT_SQL,
        (recurso, paciente, practica, DIA.replace(hour=10), DIA.replace(hour=10, minute=30)),
    )

    solapamientos = [
        (DIA.replace(hour=10, minute=15), DIA.replace(hour=10, minute=45)),  # parcial
        (DIA.replace(hour=10, minute=20), DIA.replace(hour=10, minute=40)),  # contenido
        (DIA.replace(hour=10), DIA.replace(hour=10, minute=15)),             # mismo inicio
    ]
    for inicio, fin in solapamientos:
        with pytest.raises(psycopg.errors.ExclusionViolation) as excinfo:
            with db.transaction():
                db.execute(TURNO_INSERT_SQL, (recurso, paciente, practica, inicio, fin))
        assert excinfo.value.sqlstate == "23P01"
        count = db.execute(
            "SELECT count(*) FROM reserva_agenda WHERE recurso_id = %s", (recurso,)
        ).fetchone()[0]
        assert count == 1, f"la base aceptó un solapamiento {inicio}-{fin}"
