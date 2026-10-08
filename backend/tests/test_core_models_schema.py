"""Tests de integración del esquema core (C-02 core-models-schema).

Corren contra PostgreSQL 15 real en Docker (DD-10): NUNCA SQLite ni dobles en
memoria. La fixture `migrated_database` aplica `alembic upgrade head` antes de
los tests; `db` aísla cada caso con rollback al terminar.

Tabla de mapeo spec→test: ver `SPEC_TEST_MAPPING.md` en la raíz de este grupo.
Trazabilidad: cada test cita la RN que verifica (AGENTS.md).
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from uuid import uuid4

import psycopg
import pytest

UTC = timezone.utc
DAY = datetime(2026, 1, 1, tzinfo=UTC)

TURNO_INSERT_SQL = (
    "INSERT INTO reserva_agenda "
    "(tipo, estado, recurso_id, paciente_id, practica_id, inicio, fin) "
    "VALUES ('turno', %s, %s, %s, %s, %s, %s)"
)
BLOQUEO_INSERT_SQL = (
    "INSERT INTO reserva_agenda "
    "(tipo, estado, recurso_id, paciente_id, practica_id, inicio, fin) "
    "VALUES ('bloqueo', NULL, %s, NULL, NULL, %s, %s)"
)


def at(hour: int, minute: int = 0) -> datetime:
    return DAY.replace(hour=hour, minute=minute)


def insert_recurso(conn, nombre: str = "Sillon 1"):
    return conn.execute(
        "INSERT INTO recurso (nombre) VALUES (%s) RETURNING id", (nombre,)
    ).fetchone()[0]


def insert_practica(conn, nombre: str = "Consulta", duracion_minutos: int = 30):
    return conn.execute(
        "INSERT INTO practica (nombre, duracion_minutos) VALUES (%s, %s) RETURNING id",
        (nombre, duracion_minutos),
    ).fetchone()[0]


def insert_paciente(conn, nombre: str = "Ana Perez", telefono: str = "+54-11-5555-0001"):
    return conn.execute(
        "INSERT INTO paciente (nombre, telefono) VALUES (%s, %s) RETURNING id",
        (nombre, telefono),
    ).fetchone()[0]


def insert_turno(conn, recurso_id, inicio, fin, *, estado="confirmado", paciente_id=None, practica_id=None):
    return conn.execute(
        TURNO_INSERT_SQL + " RETURNING id",
        (estado, recurso_id, paciente_id, practica_id, inicio, fin),
    ).fetchone()[0]


def insert_bloqueo(conn, recurso_id, inicio, fin):
    return conn.execute(
        BLOQUEO_INSERT_SQL + " RETURNING id", (recurso_id, inicio, fin)
    ).fetchone()[0]


def assert_db_error(conn, sql, params, exc_type):
    """Ejecuta un INSERT que debe fallar dentro de un SAVEPOINT y devuelve el error."""
    with pytest.raises(exc_type) as excinfo:
        with conn.transaction():
            conn.execute(sql, params)
    return excinfo.value


# ---------------------------------------------------------------------------
# Requisito: Migración inicial con el modelo de entidades completo
# ---------------------------------------------------------------------------


def test_migracion_crea_las_ocho_tablas_y_registra_revision(db):
    """Spec *La migración inicial crea las ocho tablas* (RN-AGE-01/02/05)."""
    expected = {
        "usuario",
        "recurso",
        "practica",
        "practicaduracion",
        "disponibilidad_semanal",
        "paciente",
        "historiaclinica",
        "reserva_agenda",
    }
    rows = db.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
    ).fetchall()
    tables = {r[0] for r in rows}
    assert expected <= tables
    # No existen tablas turno/bloqueo separadas (Opción A).
    assert "turno" not in tables
    assert "bloqueo" not in tables
    revision = db.execute("SELECT version_num FROM alembic_version").fetchone()
    assert revision is not None


def test_btree_gist_habilitado_y_constraint_exclusion_definido(db):
    """Spec *Garantía declarativa de no-solapamiento* — DDL D2."""
    ext = db.execute(
        "SELECT count(*) FROM pg_extension WHERE extname='btree_gist'"
    ).fetchone()[0]
    assert ext == 1
    row = db.execute(
        "SELECT pg_get_constraintdef(oid) FROM pg_constraint "
        "WHERE conname='reserva_agenda_sin_solapamiento' AND contype='x'"
    ).fetchone()
    assert row is not None, "falta el constraint de exclusión"
    definition = row[0]
    assert "EXCLUDE USING gist" in definition
    assert "recurso_id WITH =" in definition
    assert "tstzrange(inicio, fin, '[)'::text) WITH &&" in definition
    assert "'bloqueo'::text" in definition
    assert "'confirmado'::text" in definition


def test_integridad_referencial_obligatoria_practicaduracion_fk(db):
    """Spec *La integridad referencial es obligatoria* (RN-AGE-02)."""
    practica = insert_practica(db, "Consulta FK")
    inexistente = "00000000-0000-0000-0000-0000000000ff"
    err = assert_db_error(
        db,
        "INSERT INTO practicaduracion (practica_id, recurso_id, duracion_minutos) "
        "VALUES (%s, %s, %s)",
        (practica, inexistente, 30),
        psycopg.errors.ForeignKeyViolation,
    )
    assert err.sqlstate == "23503"
    count = db.execute(
        "SELECT count(*) FROM practicaduracion WHERE recurso_id=%s", (inexistente,)
    ).fetchone()[0]
    assert count == 0


def test_toda_fila_queda_con_timestamps(db):
    """Spec *Toda fila queda con timestamps* — created_at/updated_at en las 8 tablas."""
    usuario = db.execute(
        "INSERT INTO usuario (email, password_hash, nombre) VALUES (%s, %s, %s) RETURNING id",
        ("ts@example.com", "x" * 60, "Odontologo"),
    ).fetchone()[0]
    recurso = insert_recurso(db, "Sillon TS")
    practica = insert_practica(db, "Consulta TS")
    db.execute(
        "INSERT INTO practicaduracion (practica_id, recurso_id, duracion_minutos) VALUES (%s, %s, %s)",
        (practica, recurso, 45),
    )
    db.execute(
        "INSERT INTO disponibilidad_semanal (recurso_id, dia_semana, hora_inicio, hora_fin) "
        "VALUES (%s, %s, %s, %s)",
        (recurso, 1, "09:00", "13:00"),
    )
    paciente = insert_paciente(db, "Paciente TS", "+54-11-5555-0099")
    db.execute(
        "INSERT INTO historiaclinica (paciente_id) VALUES (%s)", (paciente,)
    )
    insert_turno(db, recurso, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)

    tablas = [
        "usuario",
        "recurso",
        "practica",
        "practicaduracion",
        "disponibilidad_semanal",
        "paciente",
        "historiaclinica",
        "reserva_agenda",
    ]
    for tabla in tablas:
        rows = db.execute(
            f"SELECT created_at, updated_at FROM {tabla}"
        ).fetchall()
        assert rows, f"{tabla} sin filas"
        for created_at, updated_at in rows:
            assert created_at is not None, f"{tabla}.created_at nulo"
            assert updated_at is not None, f"{tabla}.updated_at nulo"


# ---------------------------------------------------------------------------
# Requisito: Reservas de agenda en tabla única con discriminador tipo
# ---------------------------------------------------------------------------


def test_turno_se_persiste_con_paciente_y_practica(db):
    """Spec *Un turno se persiste con paciente y práctica* (RN-AGE-03/05)."""
    recurso = insert_recurso(db, "Sillon T")
    practica = insert_practica(db, "Consulta T")
    paciente = insert_paciente(db, "Ana T", "+54-11-5555-0002")
    turno = insert_turno(db, recurso, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)
    row = db.execute(
        "SELECT tipo, estado, paciente_id, practica_id FROM reserva_agenda WHERE id=%s",
        (turno,),
    ).fetchone()
    assert row == ("turno", "confirmado", paciente, practica)


def test_turno_sin_paciente_rechazado(db):
    """Spec *Un turno sin paciente o sin práctica es rechazado* (RN-AGE-03/05)."""
    recurso = insert_recurso(db, "Sillon SP")
    practica = insert_practica(db, "Consulta SP")
    err = assert_db_error(
        db,
        TURNO_INSERT_SQL,
        ("confirmado", recurso, None, practica, at(10), at(10, 30)),
        psycopg.errors.CheckViolation,
    )
    assert err.sqlstate == "23514"


def test_turno_sin_practica_rechazado(db):
    """Spec *Un turno sin paciente o sin práctica es rechazado* (RN-AGE-03/05)."""
    recurso = insert_recurso(db, "Sillon SPR")
    paciente = insert_paciente(db, "Ana SPR", "+54-11-5555-0003")
    err = assert_db_error(
        db,
        TURNO_INSERT_SQL,
        ("confirmado", recurso, paciente, None, at(10), at(10, 30)),
        psycopg.errors.CheckViolation,
    )
    assert err.sqlstate == "23514"


def test_bloqueo_con_paciente_rechazado(db):
    """Spec *Un bloqueo no admite datos de turno* (RN-AGE-05)."""
    recurso = insert_recurso(db, "Sillon BC")
    paciente = insert_paciente(db, "Ana BC", "+54-11-5555-0004")
    err = assert_db_error(
        db,
        "INSERT INTO reserva_agenda (tipo, estado, recurso_id, paciente_id, practica_id, inicio, fin) "
        "VALUES ('bloqueo', NULL, %s, %s, NULL, %s, %s)",
        (recurso, paciente, at(10), at(11)),
        psycopg.errors.CheckViolation,
    )
    assert err.sqlstate == "23514"


# ---------------------------------------------------------------------------
# Requisito: Garantía declarativa de no-solapamiento en reserva_agenda
# ---------------------------------------------------------------------------


def test_escritura_directa_solapada_rechazada(db):
    """Spec *Escritura directa solapada* (RN-AGE-03)."""
    recurso = insert_recurso(db, "Sillon OV")
    practica = insert_practica(db, "Consulta OV")
    paciente = insert_paciente(db, "Ana OV", "+54-11-5555-0005")
    insert_turno(db, recurso, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)
    err = assert_db_error(
        db,
        TURNO_INSERT_SQL,
        ("confirmado", recurso, paciente, practica, at(10, 15), at(10, 45)),
        psycopg.errors.ExclusionViolation,
    )
    assert err.sqlstate == "23P01"
    count = db.execute(
        "SELECT count(*) FROM reserva_agenda WHERE recurso_id=%s", (recurso,)
    ).fetchone()[0]
    assert count == 1


def test_turno_cancelado_no_ocupa_el_indice(db):
    """Spec *Un turno cancelado no ocupa el índice* (RN-AGE-03).

    El predicado parcial del EXCLUDE es `WHERE (tipo='bloqueo' OR estado='confirmado')`.
    """
    recurso = insert_recurso(db, "Sillon CX")
    practica = insert_practica(db, "Consulta CX")
    paciente = insert_paciente(db, "Ana CX", "+54-11-5555-0006")
    insert_turno(
        db, recurso, at(10), at(10, 30),
        estado="cancelado", paciente_id=paciente, practica_id=practica,
    )
    insert_turno(db, recurso, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)
    count = db.execute(
        "SELECT count(*) FROM reserva_agenda WHERE recurso_id=%s", (recurso,)
    ).fetchone()[0]
    assert count == 2


def test_turno_contra_bloqueo_rechazado(db):
    """Spec *Turno contra bloqueo del mismo recurso rechazado* (RN-AGE-05)."""
    recurso = insert_recurso(db, "Sillon TB")
    practica = insert_practica(db, "Consulta TB")
    paciente = insert_paciente(db, "Ana TB", "+54-11-5555-0007")
    insert_turno(db, recurso, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)
    err = assert_db_error(
        db,
        BLOQUEO_INSERT_SQL,
        (recurso, at(10, 15), at(11)),
        psycopg.errors.ExclusionViolation,
    )
    assert err.sqlstate == "23P01"


def test_bloqueo_contra_bloqueo_rechazado(db):
    """Spec *Bloqueo contra bloqueo del mismo recurso rechazado* (RN-AGE-05)."""
    recurso = insert_recurso(db, "Sillon BB")
    insert_bloqueo(db, recurso, at(10), at(12))
    err = assert_db_error(
        db,
        BLOQUEO_INSERT_SQL,
        (recurso, at(11), at(13)),
        psycopg.errors.ExclusionViolation,
    )
    assert err.sqlstate == "23P01"


def test_mismo_intervalo_en_otro_recurso_admitido(db):
    """Spec *Mismo intervalo en otro recurso admitido* (RN-AGE-03)."""
    r1 = insert_recurso(db, "Sillon R1")
    r2 = insert_recurso(db, "Sillon R2")
    practica = insert_practica(db, "Consulta RR")
    paciente = insert_paciente(db, "Ana RR", "+54-11-5555-0008")
    insert_turno(db, r1, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)
    insert_turno(db, r2, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)
    count = db.execute(
        "SELECT count(*) FROM reserva_agenda WHERE inicio=%s", (at(10),)
    ).fetchone()[0]
    assert count == 2


# ---------------------------------------------------------------------------
# Requisito: Intervalos semiabiertos [inicio, fin)
# ---------------------------------------------------------------------------


def test_intervalo_contiguo_admitido(db):
    """Spec *Intervalo contiguo admitido* (RN-AGE-01/03): finA == inicioB no solapa."""
    recurso = insert_recurso(db, "Sillon CT")
    practica = insert_practica(db, "Consulta CT")
    paciente = insert_paciente(db, "Ana CT", "+54-11-5555-0009")
    insert_turno(db, recurso, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)
    # 10:30 == fin del anterior -> admitido.
    insert_turno(db, recurso, at(10, 30), at(11), paciente_id=paciente, practica_id=practica)
    # 09:30-10:00 -> también admitido (precedente contiguo).
    insert_turno(db, recurso, at(9, 30), at(10), paciente_id=paciente, practica_id=practica)
    count = db.execute(
        "SELECT count(*) FROM reserva_agenda WHERE recurso_id=%s", (recurso,)
    ).fetchone()[0]
    assert count == 3


def test_mismo_instante_de_inicio_rechazado(db):
    """Spec *Mismo instante de inicio rechazado* (RN-AGE-01/03)."""
    recurso = insert_recurso(db, "Sillon MI")
    practica = insert_practica(db, "Consulta MI")
    paciente = insert_paciente(db, "Ana MI", "+54-11-5555-0010")
    insert_turno(db, recurso, at(10), at(10, 30), paciente_id=paciente, practica_id=practica)
    err = assert_db_error(
        db,
        TURNO_INSERT_SQL,
        ("confirmado", recurso, paciente, practica, at(10), at(10, 15)),
        psycopg.errors.ExclusionViolation,
    )
    assert err.sqlstate == "23P01"


def test_intervalo_invertido_o_vacio_rechazado(db):
    """Spec *Intervalo invertido o vacío rechazado* (RN-AGE-01) — CHECK (fin > inicio)."""
    recurso = insert_recurso(db, "Sillon IV")
    practica = insert_practica(db, "Consulta IV")
    paciente = insert_paciente(db, "Ana IV", "+54-11-5555-0011")
    err = assert_db_error(
        db,
        TURNO_INSERT_SQL,
        ("confirmado", recurso, paciente, practica, at(10), at(10)),
        psycopg.errors.CheckViolation,
    )
    assert err.sqlstate == "23514"
    err2 = assert_db_error(
        db,
        TURNO_INSERT_SQL,
        ("confirmado", recurso, paciente, practica, at(10), at(9)),
        psycopg.errors.CheckViolation,
    )
    assert err2.sqlstate == "23514"


# ---------------------------------------------------------------------------
# Concurrencia (spec *Dos escrituras simultáneas del mismo intervalo*)
# ---------------------------------------------------------------------------


def test_dos_escrituras_simultaneas_mismo_intervalo_un_solo_exito(migrated_database):
    """Spec *Dos escrituras simultáneas* (RN-AGE-03, RN-GEN-01).

    Dos conexiones insertan en paralelo el mismo intervalo confirmado en R:
    exactamente una tiene éxito y la otra falla con 23P01 (exclusion_violation)
    o 40P01 (deadlock_detected) — ambas prueban que sólo una escritura gana.
    Un insert del mismo intervalo en otro recurso R2 (también en paralelo) tiene
    éxito.
    """
    suffix = uuid4().hex[:8]
    setup = psycopg.connect(migrated_database)
    try:
        r1 = insert_recurso(setup, f"Sillon CONC-1-{suffix}")
        r2 = insert_recurso(setup, f"Sillon CONC-2-{suffix}")
        practica = insert_practica(setup, f"Consulta CONC {suffix}")
        paciente = insert_paciente(setup, "Ana CONC", f"+54-11-5555-{suffix}")
        setup.commit()
    finally:
        setup.close()

    try:
        results: list[str] = []
        lock = threading.Lock()
        barrier = threading.Barrier(2)

        def worker(recurso_id):
            conn = psycopg.connect(migrated_database)
            try:
                barrier.wait(timeout=10)
                try:
                    conn.execute(
                        TURNO_INSERT_SQL,
                        ("confirmado", recurso_id, paciente, practica, at(10), at(10, 30)),
                    )
                    conn.commit()
                    outcome = "ok"
                except psycopg.errors.ExclusionViolation as exc:
                    conn.rollback()
                    assert exc.sqlstate == "23P01"
                    outcome = "23P01"
                except psycopg.errors.DeadlockDetected as exc:
                    conn.rollback()
                    assert exc.sqlstate == "40P01"
                    outcome = "40P01"
                with lock:
                    results.append(outcome)
            finally:
                conn.close()

        threads = [threading.Thread(target=worker, args=(r1,)) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=15)

        losers = [r for r in results if r != "ok"]
        assert len(results) == 2, results
        assert len(losers) == 1, results
        assert losers[0] in ("23P01", "40P01"), results

        # A la par, el mismo intervalo en OTRO recurso tiene éxito.
        aux = psycopg.connect(migrated_database)
        try:
            aux.execute(
                TURNO_INSERT_SQL,
                ("confirmado", r2, paciente, practica, at(10), at(10, 30)),
            )
            aux.commit()
        finally:
            aux.close()
    finally:
        cleanup = psycopg.connect(migrated_database)
        try:
            cleanup.execute(
                "DELETE FROM reserva_agenda WHERE recurso_id IN (%s, %s)", (r1, r2)
            )
            cleanup.execute("DELETE FROM practica WHERE id=%s", (practica,))
            cleanup.execute("DELETE FROM paciente WHERE id=%s", (paciente,))
            cleanup.execute("DELETE FROM recurso WHERE id IN (%s, %s)", (r1, r2))
            cleanup.commit()
        finally:
            cleanup.close()
