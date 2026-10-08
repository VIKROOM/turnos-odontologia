"""core models schema

Revision ID: 0001_core_models_schema
Revises:
Create Date: 2026-10-06

Migración inicial del modelo relacional base (C-02 core-models-schema).

Modelo unificado (Opción A): los turnos y los bloqueos viven en la tabla única
`reserva_agenda` con el discriminador `tipo`; no existen tablas `turno` ni
`bloqueo`. La no-solapamiento la garantiza la base con un EXCLUDE USING gist
parcial sobre `reserva_agenda` (D2), habilitado por la extensión `btree_gist`.

Trazabilidad: RN-AGE-01, RN-AGE-02, RN-AGE-03, RN-AGE-05, RN-GEN-01.
"""

from alembic import op

revision = "0001_core_models_schema"
down_revision = None
branch_labels = None
depends_on = None


_UPGRADE_STATEMENTS = [
    # 1. Extensión necesaria para `WITH =` sobre escalares en un índice GiST (D2).
    "CREATE EXTENSION IF NOT EXISTS btree_gist",
    # 2. Tablas en orden topológico de FKs (D6).
    """
    CREATE TABLE usuario (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        email varchar(160) NOT NULL,
        password_hash varchar(255) NOT NULL,
        nombre varchar(120) NOT NULL,
        activo boolean NOT NULL DEFAULT true,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now(),
        CONSTRAINT usuario_email_unique UNIQUE (email)
    )
    """,
    """
    CREATE TABLE recurso (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        nombre varchar(60) NOT NULL,
        activo boolean NOT NULL DEFAULT true,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE TABLE practica (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        nombre varchar(80) NOT NULL,
        duracion_minutos integer NOT NULL,
        color varchar(7),
        activa boolean NOT NULL DEFAULT true,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now(),
        CONSTRAINT practica_nombre_unique UNIQUE (nombre),
        CONSTRAINT practica_duracion_positiva CHECK (duracion_minutos > 0)
    )
    """,
    """
    CREATE TABLE practicaduracion (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        practica_id uuid NOT NULL REFERENCES practica(id),
        recurso_id uuid NOT NULL REFERENCES recurso(id),
        duracion_minutos integer NOT NULL,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now(),
        CONSTRAINT practicaduracion_duracion_positiva CHECK (duracion_minutos > 0),
        CONSTRAINT practicaduracion_practica_recurso_unique UNIQUE (practica_id, recurso_id)
    )
    """,
    "CREATE INDEX practicaduracion_recurso_practica_idx ON practicaduracion (recurso_id, practica_id)",
    """
    CREATE TABLE disponibilidad_semanal (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        recurso_id uuid NOT NULL REFERENCES recurso(id),
        dia_semana smallint NOT NULL,
        hora_inicio time NOT NULL,
        hora_fin time NOT NULL,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now(),
        CONSTRAINT disponibilidad_semanal_dia_check CHECK (dia_semana BETWEEN 0 AND 6),
        CONSTRAINT disponibilidad_semanal_horario_check CHECK (hora_fin > hora_inicio),
        CONSTRAINT disponibilidad_semanal_recurso_dia_unique UNIQUE (recurso_id, dia_semana)
    )
    """,
    """
    CREATE TABLE paciente (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        nombre varchar(120) NOT NULL,
        telefono varchar(32) NOT NULL,
        email varchar(160),
        documento varchar(32),
        fecha_nacimiento date,
        consentimiento_salud_at timestamptz,
        consentimiento_salud_version varchar(16),
        anulado_at timestamptz,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now()
    )
    """,
    "CREATE UNIQUE INDEX paciente_telefono_activo_unique ON paciente (telefono) WHERE anulado_at IS NULL",
    """
    CREATE TABLE historiaclinica (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        paciente_id uuid NOT NULL REFERENCES paciente(id),
        abierto_at timestamptz NOT NULL DEFAULT now(),
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now()
    )
    """,
    "CREATE INDEX historiaclinica_paciente_idx ON historiaclinica (paciente_id)",
    """
    CREATE TABLE reserva_agenda (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        tipo varchar(10) NOT NULL,
        estado varchar(20),
        motivo_cancelacion text,
        token_publico varchar(64),
        recurso_id uuid NOT NULL REFERENCES recurso(id),
        paciente_id uuid REFERENCES paciente(id),
        practica_id uuid REFERENCES practica(id),
        inicio timestamptz NOT NULL,
        fin timestamptz NOT NULL,
        created_at timestamptz NOT NULL DEFAULT now(),
        updated_at timestamptz NOT NULL DEFAULT now(),
        CONSTRAINT reserva_agenda_tipo_check CHECK (tipo IN ('turno', 'bloqueo')),
        CONSTRAINT reserva_agenda_fin_mayor_inicio_check CHECK (fin > inicio),
        CONSTRAINT reserva_agenda_token_publico_unique UNIQUE (token_publico),
        CONSTRAINT reserva_agenda_discriminador_check CHECK (
            (tipo = 'turno'
                AND estado IN ('confirmado', 'cancelado', 'completado', 'no_asistio')
                AND paciente_id IS NOT NULL
                AND practica_id IS NOT NULL)
            OR
            (tipo = 'bloqueo'
                AND estado IS NULL
                AND paciente_id IS NULL
                AND practica_id IS NULL)
        )
    )
    """,
    # 3. Índices de lectura (D4).
    "CREATE INDEX reserva_agenda_recurso_idx ON reserva_agenda (recurso_id)",
    "CREATE INDEX reserva_agenda_recurso_inicio_idx ON reserva_agenda (recurso_id, inicio)",
    "CREATE INDEX reserva_agenda_paciente_idx ON reserva_agenda (paciente_id)",
    "CREATE INDEX reserva_agenda_practica_idx ON reserva_agenda (practica_id)",
    # 4. Garantía de no-solapamiento — shape D2 normativo.
    """
    ALTER TABLE reserva_agenda
      ADD CONSTRAINT reserva_agenda_sin_solapamiento
      EXCLUDE USING gist (
        recurso_id WITH =,
        tstzrange(inicio, fin, '[)') WITH &&
      )
      WHERE (tipo = 'bloqueo' OR estado = 'confirmado')
    """,
]

_DOWNGRADE_STATEMENTS = [
    "ALTER TABLE reserva_agenda DROP CONSTRAINT reserva_agenda_sin_solapamiento",
    "DROP TABLE reserva_agenda",
    "DROP TABLE historiaclinica",
    "DROP TABLE paciente",
    "DROP TABLE disponibilidad_semanal",
    "DROP TABLE practicaduracion",
    "DROP TABLE practica",
    "DROP TABLE recurso",
    "DROP TABLE usuario",
    "DROP EXTENSION IF EXISTS btree_gist",
]


def upgrade() -> None:
    for statement in _UPGRADE_STATEMENTS:
        op.execute(statement)


def downgrade() -> None:
    for statement in _DOWNGRADE_STATEMENTS:
        op.execute(statement)
