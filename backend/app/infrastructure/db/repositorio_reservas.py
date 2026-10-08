import psycopg

from app.domain.agenda import Intervalo, SolapamientoDetectado


class RepositorioReservas:
    """Acceso a `reserva_agenda` / catálogos: único punto que conoce la BD (D3).

    Sólo lee recurso/práctica/duración y escribe turnos `tipo='turno'`,
    `estado='confirmado'` desde el nacimiento (design Open Questions 1).
    """

    def __init__(self, conn: psycopg.Connection):
        self._conn = conn

    def duracion_de_practica(self, *, practica_id, recurso_id) -> int:
        """RN-AGE-01: la duración se deriva de la práctica, nunca del cliente.

        Toma el override por recurso (`practicaduracion`) si existe; si no, la
        configuración global de la práctica (`practica.duracion_minutos`).
        """
        fila = self._conn.execute(
            """
            SELECT COALESCE(pd.duracion_minutos, p.duracion_minutos)
              FROM practica p
              LEFT JOIN practicaduracion pd
                ON pd.practica_id = p.id AND pd.recurso_id = %s
             WHERE p.id = %s
            """,
            (recurso_id, practica_id),
        ).fetchone()
        return int(fila[0])

    def reservas_solapadas(self, *, recurso_id, inicio, fin) -> list[Intervalo]:
        """Reservas efectivas del mismo recurso que intersectan `[inicio, fin)`.

        Filtra a la red de seguridad de la base (mismo predicado parcial de
        `reserva_agenda_sin_solapamiento`): turnos `confirmado` y bloqueos.
        """
        filas = list(self._conn.execute(
            """
            SELECT recurso_id, inicio, fin
              FROM reserva_agenda
             WHERE recurso_id = %(recurso_id)s
               AND inicio < %(fin_nuevo)s
               AND fin > %(inicio_nuevo)s
               AND (tipo = 'bloqueo' OR estado = 'confirmado')
            """,
            {"recurso_id": recurso_id, "inicio_nuevo": inicio, "fin_nuevo": fin},
        ))
        return [Intervalo(recurso_id=fila[0], inicio=fila[1], fin=fila[2]) for fila in filas]

    def insertar_turno(self, *, recurso_id, paciente_id, practica_id, inicio, fin) -> dict:
        try:
            fila = self._conn.execute(
                """
                INSERT INTO reserva_agenda
                    (tipo, estado, recurso_id, paciente_id, practica_id, inicio, fin)
                VALUES ('turno', 'confirmado', %s, %s, %s, %s, %s)
                RETURNING id, recurso_id, paciente_id, practica_id, inicio, fin, estado
                """,
                (recurso_id, paciente_id, practica_id, inicio, fin),
            ).fetchone()
        except (psycopg.errors.ExclusionViolation, psycopg.errors.DeadlockDetected) as error:
            # D4 / RN-GEN-05: tanto la violación del constraint (23P01) como el
            # aborto por detector de deadlock del perdedor de una escritura
            # concurrente (40P01) son conflicto de solapamiento, nunca un
            # éxito — la API los responderá como 409.
            raise SolapamientoDetectado(
                "El intervalo solicitado está ocupado en este recurso."
            ) from error
        return {
            "id": fila[0],
            "recurso_id": fila[1],
            "paciente_id": fila[2],
            "practica_id": fila[3],
            "inicio": fila[4],
            "fin": fila[5],
            "estado": fila[6],
        }
