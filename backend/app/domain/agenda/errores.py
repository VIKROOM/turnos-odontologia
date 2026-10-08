class SolapamientoDetectado(Exception):
    """Error de dominio (design D4): el intervalo pedido se solapa con una reserva.

    Se origina en la validación de dominio (primera línea UX, RN-AGE-03) o en
    la violación de exclusión de la base (23P01, RN-GEN-01) — nunca es un éxito.
    La API lo expone como HTTP 409 (RN-GEN-05).
    """