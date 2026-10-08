from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Intervalo:
    """Reserva de agenda como intervalo semiabierto `[inicio, fin)` de un recurso."""

    recurso_id: object
    inicio: datetime
    fin: datetime


def solapan(a: Intervalo, b: Intervalo) -> bool:
    """RN-AGE-03: True si los intervalos del MISMO recurso se intersectan.

    Semántica semiabierta `[inicio, fin)`: `finA == inicioB` NO solapa;
    `inicioA == inicioB` SÍ solapa. Intervalos de recursos distintos nunca se
    comparan — cada recurso (sillón/box) tiene su propia agenda.
    """
    return _mismo_recurso(a, b) and _se_intersectan(a, b)


def _mismo_recurso(a: Intervalo, b: Intervalo) -> bool:
    return a.recurso_id == b.recurso_id


def _se_intersectan(a: Intervalo, b: Intervalo) -> bool:
    return a.inicio < b.fin and b.inicio < a.fin
