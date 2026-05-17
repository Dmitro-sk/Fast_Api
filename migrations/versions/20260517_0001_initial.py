"""Initial database schema and seed data.

Revision ID: 20260517_0001
Revises:
Create Date: 2026-05-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260517_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users = op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    profiles = op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("experience_years", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    categories = op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    teams = op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("country", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    motorcycles = op.create_table(
        "motorcycles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.bulk_insert(
        users,
        [
            {"id": 1, "username": "andrii", "email": "andrii@example.com", "password": "secret123"},
            {"id": 2, "username": "olena", "email": "olena@example.com", "password": "secret456"},
        ],
    )
    op.bulk_insert(
        profiles,
        [
            {"id": 1, "bio": "Sport rider", "experience_years": 4, "user_id": 1},
            {"id": 2, "bio": "Touring fan", "experience_years": 7, "user_id": 2},
        ],
    )
    op.bulk_insert(
        categories,
        [
            {"id": 1, "name": "Sport"},
            {"id": 2, "name": "Touring"},
        ],
    )
    op.bulk_insert(
        teams,
        [
            {"id": 1, "name": "Kyiv Riders", "country": "Ukraine"},
            {"id": 2, "name": "Lviv Garage", "country": "Ukraine"},
        ],
    )
    op.bulk_insert(
        motorcycles,
        [
            {"id": 1, "model_name": "Yamaha R7", "year": 2023, "owner_id": 1, "category_id": 1, "team_id": 1},
            {"id": 2, "model_name": "Honda NC750X", "year": 2022, "owner_id": 2, "category_id": 2, "team_id": 2},
        ],
    )
    op.execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));")
    op.execute("SELECT setval('profiles_id_seq', (SELECT MAX(id) FROM profiles));")
    op.execute("SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));")
    op.execute("SELECT setval('teams_id_seq', (SELECT MAX(id) FROM teams));")
    op.execute("SELECT setval('motorcycles_id_seq', (SELECT MAX(id) FROM motorcycles));")


def downgrade() -> None:
    op.drop_table("motorcycles")
    op.drop_table("teams")
    op.drop_table("categories")
    op.drop_table("profiles")
    op.drop_table("users")
