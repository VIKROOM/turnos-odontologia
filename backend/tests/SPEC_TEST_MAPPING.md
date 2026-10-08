# Mapa spec → test — `core/data-model` (C-02 core-models-schema)

Todos los tests corren en `test_core_models_schema.py` contra PostgreSQL 15 real
en Docker (DD-10). La fixture `migrated_database` aplica `alembic upgrade head`;
`db` aísla cada caso por rollback.

| Requirement (spec) | Scenario | Test | RN | SQLSTATE |
|---|---|---|---|---|
| Migración inicial con el modelo de entidades completo | La migración inicial crea las ocho tablas | `test_migracion_crea_las_ocho_tablas_y_registra_revision` | RN-AGE-01/02/05 | — |
| Migración inicial con el modelo de entidades completo | La integridad referencial es obligatoria | `test_integridad_referencial_obligatoria_practicaduracion_fk` | RN-AGE-02 | `23503` |
| Migración inicial con el modelo de entidades completo | Toda fila queda con timestamps | `test_toda_fila_queda_con_timestamps` | RN-AGE-01 | — |
| Reservas de agenda en tabla única con discriminador `tipo` | Un turno se persiste con paciente y práctica | `test_turno_se_persiste_con_paciente_y_practica` | RN-AGE-03/05 | — |
| Reservas de agenda en tabla única con discriminador `tipo` | Un turno sin paciente o sin práctica es rechazado | `test_turno_sin_paciente_rechazado`, `test_turno_sin_practica_rechazado` | RN-AGE-03/05 | `23514` |
| Reservas de agenda en tabla única con discriminador `tipo` | Un bloqueo no admite datos de turno | `test_bloqueo_con_paciente_rechazado` | RN-AGE-05 | `23514` |
| Garantía declarativa de no-solapamiento en `reserva_agenda` | Escritura directa solapada rechazada por la base | `test_escritura_directa_solapada_rechazada` | RN-AGE-03 | `23P01` |
| Garantía declarativa de no-solapamiento en `reserva_agenda` | Un turno cancelado no ocupa el índice | `test_turno_cancelado_no_ocupa_el_indice` | RN-AGE-03 | — |
| Garantía declarativa de no-solapamiento en `reserva_agenda` | Turno contra bloqueo del mismo recurso rechazado | `test_turno_contra_bloqueo_rechazado` | RN-AGE-05 | `23P01` |
| Garantía declarativa de no-solapamiento en `reserva_agenda` | Bloqueo contra bloqueo del mismo recurso rechazado | `test_bloqueo_contra_bloqueo_rechazado` | RN-AGE-05 | `23P01` |
| Garantía declarativa de no-solapamiento en `reserva_agenda` | Mismo intervalo en otro recurso admitido | `test_mismo_intervalo_en_otro_recurso_admitido` | RN-AGE-03 | — |
| Garantía declarativa de no-solapamiento en `reserva_agenda` | Dos escrituras simultáneas del mismo intervalo — un solo éxito | `test_dos_escrituras_simultaneas_mismo_intervalo_un_solo_exito` | RN-AGE-03, RN-GEN-01 | `23P01` |
| Intervalos semiabiertos `[inicio, fin)` a nivel de base | Intervalo contiguo admitido | `test_intervalo_contiguo_admitido` | RN-AGE-01/03 | — |
| Intervalos semiabiertos `[inicio, fin)` a nivel de base | Mismo instante de inicio rechazado | `test_mismo_instante_de_inicio_rechazado` | RN-AGE-01/03 | `23P01` |
| Intervalos semiabiertos `[inicio, fin)` a nivel de base | Intervalo invertido o vacío rechazado | `test_intervalo_invertido_o_vacio_rechazado` | RN-AGE-01 | `23514` |

Verificación adicional del DDL normativo (design D2), fuera de los escenarios del
spec pero exigida por la tarea 3.2: `test_btree_gist_habilitado_y_constraint_exclusion_definido`
comprueba que la extensión `btree_gist` existe y que
`reserva_agenda_sin_solapamiento` es un `EXCLUDE USING gist` con
`recurso_id WITH =`, `tstzrange(inicio, fin, '[)') WITH &&` y el predicado parcial.
