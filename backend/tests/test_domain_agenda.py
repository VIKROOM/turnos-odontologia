"""Tests unitarios del dominio de agenda — funciones puras, sin base (design D5).

La aritmética de intervalos y la convención `[inicio, fin)` viven en
`app/domain/agenda/` sin I/O ni imports de `infrastructure/` (AGENTS.md).
La garantía de no-solapamiento NO se prueba acá: esa vive en PostgreSQL real
(DD-05/DD-10); acá sólo se prueba la lógica pura que la primera línea de UX
usa antes de tocar la base.

Trazabilidad: RN-AGE-01 (duración derivada de la práctica), RN-AGE-03
(semántica de solapamiento por recurso).
"""

from datetime import datetime, timezone
from uuid import uuid4

from app.domain import agenda

DIA = datetime(2026, 3, 2, tzinfo=timezone.utc)
SILLON_1 = uuid4()
SILLON_2 = uuid4()


def test_fin_derivado_de_practica():
    """RN-AGE-01: inicio 10:00 + práctica de 30 min => fin 10:30.

    Escenario *Camino feliz*: la duración la fija la práctica, nunca un valor
    libre del cliente.
    """
    inicio = DIA.replace(hour=10)

    fin = agenda.calcular_fin(inicio, duracion_minutos=30)

    assert fin == DIA.replace(hour=10, minute=30)


def test_fin_de_fin_no_solapa():
    """RN-AGE-03: `finA == inicioB` NO solapa — semántica `[inicio, fin)`."""
    a = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10), fin=DIA.replace(hour=10, minute=30))
    b = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10, minute=30), fin=DIA.replace(hour=11))

    assert agenda.solapan(a, b) is False


def test_mismo_inicio_si_solapa():
    """RN-AGE-03: `inicioA == inicioB` SÍ solapa — el extremo izquierdo es cerrado."""
    a = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10), fin=DIA.replace(hour=10, minute=30))
    b = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10), fin=DIA.replace(hour=11))

    assert agenda.solapan(a, b) is True


def test_mismo_intervalo_en_otro_recurso_no_compara():
    """RN-AGE-03: turnos en recursos distintos no se comparan entre sí."""
    a = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10), fin=DIA.replace(hour=10, minute=30))
    b = agenda.Intervalo(recurso_id=SILLON_2, inicio=DIA.replace(hour=10), fin=DIA.replace(hour=10, minute=30))

    assert agenda.solapan(a, b) is False


def test_intervalo_contenido_solapa():
    """RN-AGE-03 (triangulación): un intervalo estrictamente contenido solapa."""
    a = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10), fin=DIA.replace(hour=11))
    b = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10, minute=20), fin=DIA.replace(hour=10, minute=40))

    assert agenda.solapan(a, b) is True
    assert agenda.solapan(b, a) is True


def test_intervalos_disjuntos_no_solapan():
    """RN-AGE-03 (triangulación): intervalos separados no solapan."""
    a = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10), fin=DIA.replace(hour=10, minute=30))
    b = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=11), fin=DIA.replace(hour=11, minute=30))

    assert agenda.solapan(a, b) is False
    assert agenda.solapan(b, a) is False


def test_b_termina_donde_a_empieza_no_solapa():
    """RN-AGE-03 (triangulación): `finB == inicioA` tampoco solapa — simetría."""
    a = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=11), fin=DIA.replace(hour=11, minute=30))
    b = agenda.Intervalo(recurso_id=SILLON_1, inicio=DIA.replace(hour=10), fin=DIA.replace(hour=11))

    assert agenda.solapan(a, b) is False
    assert agenda.solapan(b, a) is False
