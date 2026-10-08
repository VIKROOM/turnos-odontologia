from datetime import datetime, timedelta


def calcular_fin(inicio: datetime, duracion_minutos: int) -> datetime:
    """RN-AGE-01: `fin = inicio + duración(práctica)`.

    La duración la aporta la configuración de la práctica (o su override por
    recurso en `practicaduracion`); nunca es un valor libre del cliente.
    """
    return inicio + timedelta(minutes=duracion_minutos)
