from app.domain.agenda import Intervalo, SolapamientoDetectado, calcular_fin, solapan


class CrearTurnoServicio:
    """Caso de uso crear turno (design D3).

    RN-GEN-04: la validación de disponibilidad ocurre en el servidor, nunca
    sólo en el navegador. Orquesta: dominio (duración → fin, RN-AGE-01, y
    solapamiento por recurso, RN-AGE-03) ANTES de persistir; la violación de
    exclusión de la base se traduce a error de dominio tipado (design D4).
    """

    def __init__(self, repositorio):
        self._repositorio = repositorio

    def crear_turno(self, *, recurso_id, paciente_id, practica_id, hora_inicio) -> dict:
        duracion = self._repositorio.duracion_de_practica(
            practica_id=practica_id, recurso_id=recurso_id
        )
        fin = calcular_fin(hora_inicio, duracion)
        nuevo = Intervalo(recurso_id=recurso_id, inicio=hora_inicio, fin=fin)
        for existente in self._repositorio.reservas_solapadas(
            recurso_id=recurso_id, inicio=hora_inicio, fin=fin
        ):
            if solapan(nuevo, existente):
                raise SolapamientoDetectado("El intervalo solicitado está ocupado en este recurso.")
        return self._repositorio.insertar_turno(
            recurso_id=recurso_id,
            paciente_id=paciente_id,
            practica_id=practica_id,
            inicio=hora_inicio,
            fin=fin,
        )