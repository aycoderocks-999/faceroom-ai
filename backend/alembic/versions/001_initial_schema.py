"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-09

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_name", sa.String(length=200), nullable=False),
        sa.Column("room_code", sa.String(length=20), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rooms_id"), "rooms", ["id"], unique=False)
    op.create_index(op.f("ix_rooms_room_code"), "rooms", ["room_code"], unique=True)

    op.create_table(
        "room_members",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_room_members_id"), "room_members", ["id"], unique=False)
    op.create_index(op.f("ix_room_members_room_id"), "room_members", ["room_id"], unique=False)
    op.create_index(op.f("ix_room_members_user_id"), "room_members", ["user_id"], unique=False)

    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("uploader_id", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=False),
        sa.Column("storage_path", sa.String(length=500), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column(
            "processing_status",
            sa.Enum("PENDING", "PROCESSING", "COMPLETED", "FAILED", name="processingstatus"),
            nullable=False,
        ),
        sa.Column("upload_time", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.ForeignKeyConstraint(["uploader_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_images_id"), "images", ["id"], unique=False)
    op.create_index(op.f("ix_images_room_id"), "images", ["room_id"], unique=False)

    op.create_table(
        "face_clusters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("representative_face_id", sa.Integer(), nullable=True),
        sa.Column("representative_face_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_face_clusters_id"), "face_clusters", ["id"], unique=False)
    op.create_index(op.f("ix_face_clusters_room_id"), "face_clusters", ["room_id"], unique=False)

    op.create_table(
        "faces",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=False),
        sa.Column("embedding_id", sa.String(length=100), nullable=False),
        sa.Column("cluster_id", sa.Integer(), nullable=True),
        sa.Column("bounding_box", sa.JSON(), nullable=False),
        sa.Column("quality_score", sa.Float(), nullable=True),
        sa.Column("crop_url", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["cluster_id"], ["face_clusters.id"]),
        sa.ForeignKeyConstraint(["image_id"], ["images.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_faces_cluster_id"), "faces", ["cluster_id"], unique=False)
    op.create_index(op.f("ix_faces_embedding_id"), "faces", ["embedding_id"], unique=True)
    op.create_index(op.f("ix_faces_id"), "faces", ["id"], unique=False)
    op.create_index(op.f("ix_faces_image_id"), "faces", ["image_id"], unique=False)

    op.create_foreign_key("fk_face_clusters_representative", "face_clusters", "faces", ["representative_face_id"], ["id"])

    op.create_table(
        "search_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("latency_ms", sa.Float(), nullable=False),
        sa.Column("result_count", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_search_logs_id"), "search_logs", ["id"], unique=False)
    op.create_index(op.f("ix_search_logs_room_id"), "search_logs", ["room_id"], unique=False)
    op.create_index(op.f("ix_search_logs_user_id"), "search_logs", ["user_id"], unique=False)

    op.create_table(
        "processing_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=False),
        sa.Column("celery_task_id", sa.String(length=100), nullable=True),
        sa.Column(
            "status",
            sa.Enum("QUEUED", "RUNNING", "COMPLETED", "FAILED", "RETRYING", name="taskstatus"),
            nullable=False,
        ),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["image_id"], ["images.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_processing_tasks_id"), "processing_tasks", ["id"], unique=False)
    op.create_index(op.f("ix_processing_tasks_image_id"), "processing_tasks", ["image_id"], unique=False)


def downgrade() -> None:
    op.drop_table("processing_tasks")
    op.drop_table("search_logs")
    op.drop_table("faces")
    op.drop_table("face_clusters")
    op.drop_table("images")
    op.drop_table("room_members")
    op.drop_table("rooms")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS taskstatus")
    op.execute("DROP TYPE IF EXISTS processingstatus")
