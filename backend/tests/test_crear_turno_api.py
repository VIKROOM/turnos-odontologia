"""Tests de integración de creación de turno — API + PostgreSQL real (D5/DD-10).

Camino completo: Pydantic (borde) -> caso de uso -> repositorio ->
`reserva_agenda`. NUNCA SQLite ni dobles en memoria: la garantía de
no-solapamiento sólo existe en postgres:15-alpine.

Trazabilidad: RN-AGE-01 (duración de la práctica), RN-AGE-03 (solapamiento),
RN-GEN-01 (concurrencia arbitra por la base), RN-GEN-04 (el servidor valida
aunque el cliente no), RN-GEN-05 (409 sin éxito falso).
"""

import threading
from datetime import datetime, timezone

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.infrastructure.db.repositorio_reservas import RepositorioReservas
from app.main import app

INICIO_ESPERADO = datetime(2026, 3, 2, 10, 0, tzinfo=timezone.utc)
FIN_ESPERADO = datetime(2026, 3, 2, 10, 30, tzinfo=timezone.utc)
HORA_10 = "2026-03-02T10:00:00+00:00"


def payload(seed, hora: str = HORA_10, *, practica=None, recurso=None) -> dict:
    return {
        "recurso_id": str(recurso or seed.recurso1),
        "paciente_id": str(seed.paciente),
        "practica_id": str(practica or seed.practica30),
        "hora_inicio": hora,
    }


def contar_reservas(database_url: str, recurso_id) -> int:
    conn = psycopg.connect(database_url, autocommit=True)
    try:
        return conn.execute(
            "SELECT count(*) FROM reserva_agenda WHERE recurso_id = %s", (recurso_id,)
        ).fetchone()[0]
    finally:
        conn.close()


def post_en_paralelo(*cuerpos: dict) -> list[str]:
    """Envía un POST por cuerpo, sincronizados por barrera; devuelve los status.

    Cada hilo usa su propio `TestClient` (y por ende su propia conexión a la
    base vía `transaccion()`), de modo que las escrituras compiten de verdad
    contra el mismo PostgreSQL (DD-10).
    """
    barrera = threading.Barrier(len(cuerpos), timeout=15)
    resultados: list[str] = []
    lock = threading.Lock()

    def worker(cuerpo: dict):
        cliente = TestClient(app, raise_server_exceptions=False)
        try:
            barrera.wait()
            codigo = str(cliente.post("/turnos", json=cuerpo).status_code)
        except Exception as error:  # noqa: BLE001 — el fallo se reporta en la aserción
            codigo = f"EXC:{error!r}"
        with lock:
            resultados.append(codigo)

    hilos = [threading.Thread(target=worker, args=(cuerpo,)) for cuerpo in cuerpos]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join(timeout=30)
    assert len(resultados) == len(cuerpos), resultados
    return sorted(resultados)


def test_camino_feliz_turno_creado_y_persistido(client, agenda_seed, database_url):
    """RN-AGE-01 — Escenario *Camino feliz*: turno 10:00-10:30 en sillón 1.

    La duración la fija la práctica (30 min); el turno nace `confirmado` y una
    lectura posterior devuelve los mismos valores.
    """
    resp = client.post("/turnos", json=payload(agenda_seed))

    assert resp.status_code == 201, resp.text
    cuerpo = resp.json()
    assert datetime.fromisoformat(cuerpo["inicio"]) == INICIO_ESPERADO
    assert datetime.fromisoformat(cuerpo["fin"]) == FIN_ESPERADO
    assert cuerpo["estado"] == "confirmado"

    conn = psycopg.connect(database_url, autocommit=True)
    try:
        fila = conn.execute(
            "SELECT tipo, estado, inicio, fin FROM reserva_agenda WHERE id = %s",
            (cuerpo["id"],),
        ).fetchone()
    finally:
        conn.close()
    assert fila == ("turno", "confirmado", INICIO_ESPERADO, FIN_ESPERADO)


def test_solapamiento_parcial_rechazado(client, agenda_seed, database_url):
    """RN-AGE-03 — Escenario *Solapamiento parcial rechazado* (5.3).

    Existe 10:00-10:30 en sillón 1; crear 10:15-10:45 → 409 con mensaje claro.
    """
    assert client.post("/turnos", json=payload(agenda_seed)).status_code == 201

    resp = client.post(
        "/turnos",
        json=payload(agenda_seed, hora="2026-03-02T10:15:00+00:00"),
    )

    assert resp.status_code == 409, resp.text
    detalle = resp.json()["detail"].lower()
    assert "intervalo" in detalle and "ocupado" in detalle
    assert contar_reservas(database_url, agenda_seed.recurso1) == 1


def test_intervalo_contenido_rechazado(client, agenda_seed, database_url):
    """RN-AGE-03 — Escenario *Intervalo contenido rechazado* (5.4).

    Existe 10:00-11:00 (práctica de 60'); crear 10:20-10:40 → 409.
    """
    ok = client.post(
        "/turnos",
        json=payload(agenda_seed, practica=agenda_seed.practica60),
    )
    assert ok.status_code == 201, ok.text

    resp = client.post(
        "/turnos",
        json=payload(agenda_seed, hora="2026-03-02T10:20:00+00:00"),
    )

    assert resp.status_code == 409, resp.text
    assert contar_reservas(database_url, agenda_seed.recurso1) == 1


def test_servidor_valida_aunque_cliente_no(client, agenda_seed, database_url):
    """RN-GEN-04 — Escenario *El servidor valida aunque el cliente no* (5.6).

    El cliente omite cualquier chequeo previo de disponibilidad; el servidor
    igual rechaza con 409.
    """
    assert client.post("/turnos", json=payload(agenda_seed)).status_code == 201

    resp = client.post(
        "/turnos",
        json=payload(
            agenda_seed,
            hora="2026-03-02T10:10:00+00:00",
            practica=agenda_seed.practica10,
        ),
    )

    assert resp.status_code == 409, resp.text
    assert contar_reservas(database_url, agenda_seed.recurso1) == 1


@pytest.mark.parametrize(
    "campo_libre",
    ["duracion", "duracion_minutos", "fin"],
)
def test_duracion_no_es_parametro_libre_del_cliente(client, agenda_seed, database_url, campo_libre):
    """RN-AGE-01 — Escenario *La duración no es un parámetro libre del cliente* (5.2).

    La duración (y el fin) se deriva de la práctica; el cliente NO puede
    fijarla. Cualquier campo que la fuerce responde 422 y no persiste nada.
    """
    cuerpo = payload(agenda_seed)
    cuerpo[campo_libre] = "2026-03-02T11:00:00+00:00" if campo_libre == "fin" else 60

    resp = client.post("/turnos", json=cuerpo)

    assert resp.status_code == 422, resp.text
    assert contar_reservas(database_url, agenda_seed.recurso1) == 0


def test_mismo_intervalo_en_otro_recurso_permitido(client, agenda_seed, database_url):
    """RN-AGE-03 — Escenario *Mismo intervalo en otro recurso permitido* (5.5).

    El sillón 1 ocupado 10:00-10:30 no impide el mismo intervalo en sillón 2:
    los recursos se comparan por separado.
    """
    assert client.post("/turnos", json=payload(agenda_seed)).status_code == 201

    resp = client.post(
        "/turnos", json=payload(agenda_seed, recurso=agenda_seed.recurso2)
    )

    assert resp.status_code == 201, resp.text
    assert contar_reservas(database_url, agenda_seed.recurso2) == 1


def test_turno_empieza_cuando_otro_termina_aceptado(client, agenda_seed, database_url):
    """RN-AGE-01, RN-AGE-03 — Escenario *Turno que empieza cuando otro termina*
    (5.7).

    Semántica `[inicio, fin)`: existe 10:00-10:30; crear 10:30-11:00 no se
    solapa y debe quedar persistido.
    """
    assert client.post("/turnos", json=payload(agenda_seed)).status_code == 201

    resp = client.post(
        "/turnos", json=payload(agenda_seed, hora="2026-03-02T10:30:00+00:00")
    )

    assert resp.status_code == 201, resp.text
    assert contar_reservas(database_url, agenda_seed.recurso1) == 2


def test_turno_termina_cuando_otro_empieza_aceptado(client, agenda_seed, database_url):
    """RN-AGE-01, RN-AGE-03 — Escenario *Turno que termina cuando otro empieza*
    (5.8).

    Existe 10:30-11:00; crear 10:00-10:30 toca el borde derecho sin
    solaparse: debe quedar persistido.
    """
    assert client.post(
        "/turnos", json=payload(agenda_seed, hora="2026-03-02T10:30:00+00:00")
    ).status_code == 201

    resp = client.post("/turnos", json=payload(agenda_seed))

    assert resp.status_code == 201, resp.text
    assert contar_reservas(database_url, agenda_seed.recurso1) == 2


def test_turno_empieza_cuando_otro_empieza_rechazado(client, agenda_seed, database_url):
    """RN-AGE-03 — Escenario *Turno que empieza cuando otro empieza —
    rechazado* (5.9).

    El extremo izquierdo del intervalo es cerrado: compartir el instante de
    inicio es solapamiento y responde 409.
    """
    assert client.post("/turnos", json=payload(agenda_seed)).status_code == 201

    resp = client.post("/turnos", json=payload(agenda_seed))

    assert resp.status_code == 409, resp.text
    detalle = resp.json()["detail"].lower()
    assert "intervalo" in detalle and "ocupado" in detalle
    assert contar_reservas(database_url, agenda_seed.recurso1) == 1


def test_escritura_falla_en_la_base_responde_409_sin_exito(
    client, agenda_seed, database_url, monkeypatch
):
    """RN-GEN-05 — Escenario *Violación de exclusión responde 409 sin éxito
    falso* (5.13 / tareas 4.3-4.4).

    Simula la carrera perdida: la validación de dominio no ve la reserva
    existente (check previo fallido) y el INSERT choca con el constraint ->
    23P01 en la escritura -> HTTP 409 con mensaje de intervalo ocupado,
    nunca una confirmación de creación.
    """
    assert client.post("/turnos", json=payload(agenda_seed)).status_code == 201
    monkeypatch.setattr(
        RepositorioReservas, "reservas_solapadas", lambda self, **kwargs: []
    )

    resp = client.post(
        "/turnos",
        json=payload(agenda_seed, hora="2026-03-02T10:15:00+00:00"),
    )

    assert resp.status_code == 409, resp.text
    assert "id" not in resp.json(), "una escritura fallida no puede reportar creación"
    detalle = resp.json()["detail"].lower()
    assert "intervalo" in detalle and "ocupado" in detalle
    assert contar_reservas(database_url, agenda_seed.recurso1) == 1


def test_deadlock_en_la_escritura_responde_409_sin_exito(
    client, agenda_seed, database_url, monkeypatch
):
    """RN-GEN-05 / design D4 — `40P01` (deadlock_detected) en la escritura
    también responde 409, nunca éxito ni 500.

    En una carrera real el detector de deadlock de PostgreSQL aborta al
    perdedor con 40P01 en lugar de 23P01 (~20% de las corridas): se simula
    ese aborto en el borde del driver para el INSERT, y el resto del camino
    (dominio -> repositorio -> router) es el real. El chequeo de dominio se
    anula para que el conflicto llegue sí o sí a la escritura.
    """
    assert client.post("/turnos", json=payload(agenda_seed)).status_code == 201
    monkeypatch.setattr(
        RepositorioReservas, "reservas_solapadas", lambda self, **kwargs: []
    )

    execute_real = psycopg.Connection.execute

    def execute_con_deadlock(self, query, params=None, *args, **kwargs):
        if str(query).lstrip().upper().startswith("INSERT INTO RESERVA_AGENDA"):
            raise psycopg.errors.DeadlockDetected("deadlock detected")
        return execute_real(self, query, params, *args, **kwargs)

    monkeypatch.setattr(psycopg.Connection, "execute", execute_con_deadlock)

    resp = client.post(
        "/turnos",
        json=payload(agenda_seed, hora="2026-03-02T10:15:00+00:00"),
    )

    assert resp.status_code == 409, resp.text
    assert "id" not in resp.json(), "una escritura fallida no puede reportar creación"
    detalle = resp.json()["detail"].lower()
    assert "intervalo" in detalle and "ocupado" in detalle
    assert contar_reservas(database_url, agenda_seed.recurso1) == 1


def test_escrituras_simultaneas_mismo_intervalo_un_solo_exito(
    client, agenda_seed, database_url
):
    """RN-AGE-01, RN-GEN-01 — Escenario *Dos escrituras simultáneas del mismo
    intervalo — un solo éxito* (5.10 / tareas 4.5-4.6).

    10 corridas seguidas contra postgres:15-alpine: en cada una dos clientes
    envían la misma creación en paralelo y el resultado es exactamente
    1×201 + 1×409. El perdedor lo decide PostgreSQL (23P01 o 40P01) y el
    mapeo D4 lo traduce a 409 en ambos casos.
    """
    for corrida in range(10):
        hora = f"2026-03-02T{10 + corrida}:00:00+00:00"
        cuerpo = payload(agenda_seed, hora=hora)

        assert post_en_paralelo(cuerpo, dict(cuerpo)) == ["201", "409"], (
            f"corrida {corrida}: esperaba 1×201 + 1×409"
        )
    assert contar_reservas(database_url, agenda_seed.recurso1) == 10


def test_escrituras_simultaneas_recursos_distintos_ambas_exitosas(
    client, agenda_seed, database_url
):
    """RN-AGE-01, RN-GEN-01 — Escenario *Escrituras simultáneas en recursos
    distintos — ambas exitosas* (5.11 / tarea 4.7).

    5 corridas: sillón 1 y sillón 2 reciben el mismo intervalo en paralelo y
    ambas creaciones reportan éxito (la exclusión es por recurso).
    """
    for corrida in range(5):
        hora = f"2026-03-02T{10 + corrida}:00:00+00:00"

        assert post_en_paralelo(
            payload(agenda_seed, hora=hora),
            payload(agenda_seed, hora=hora, recurso=agenda_seed.recurso2),
        ) == ["201", "201"], f"corrida {corrida}: esperaba 2×201"
    assert contar_reservas(database_url, agenda_seed.recurso1) == 5
    assert contar_reservas(database_url, agenda_seed.recurso2) == 5
