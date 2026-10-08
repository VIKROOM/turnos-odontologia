from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from app.application.services.crear_turno import CrearTurnoServicio
from app.domain.agenda import SolapamientoDetectado
from app.infrastructure.db.conexion import transaccion
from app.infrastructure.db.repositorio_reservas import RepositorioReservas

router = APIRouter(prefix="/turnos", tags=["turnos"])


class SolicitudCrearTurno(BaseModel):
    """RN-AGE-01: la duración NO es un parámetro libre del cliente.

    `extra="forbid"` rechaza (422) cualquier campo que pretenda fijar
    duración/fin (`duracion`, `duracion_minutos`, `fin`): el fin se deriva
    exclusivamente de la práctica configurada.
    """

    model_config = ConfigDict(extra="forbid")

    recurso_id: UUID
    paciente_id: UUID
    practica_id: UUID
    hora_inicio: datetime


@router.post("", status_code=201)
def crear_turno(solicitud: SolicitudCrearTurno) -> dict:
    """POST /turnos — creación de turno con validación en el servidor (RN-GEN-04).

    El conflicto de exclusión (de dominio o de la base, 23P01) se mapea a
    HTTP 409 con mensaje claro de intervalo ocupado (D4, RN-GEN-05); nunca se
    reporta éxito sin confirmación de escritura.
    """
    try:
        with transaccion() as conn:
            servicio = CrearTurnoServicio(RepositorioReservas(conn))
            return servicio.crear_turno(
                recurso_id=solicitud.recurso_id,
                paciente_id=solicitud.paciente_id,
                practica_id=solicitud.practica_id,
                hora_inicio=solicitud.hora_inicio,
            )
    except SolapamientoDetectado as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
