"""Hash seeded user passwords.

Revision ID: 20260519_0002
Revises: 20260517_0001
Create Date: 2026-05-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260519_0002"
down_revision: Union[str, Sequence[str], None] = "20260517_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "password",
        existing_type=sa.String(length=100),
        type_=sa.String(length=255),
        existing_nullable=False,
    )
    op.execute(
        """
        UPDATE users
        SET password = 'pbkdf2_sha256$260000$060f7158b0fab874163bab919bef7dad$17299fd6f3252ff2295c86a5752b77f4c85c1617567842890e34f9659855a53b'
        WHERE username = 'andrii' AND password = 'secret123';
        """,
    )
    op.execute(
        """
        UPDATE users
        SET password = 'pbkdf2_sha256$260000$667e887685f3ca4913fd1c3221508ece$8b9f8d55c8892d1ffacdf7caeb7450b6e5e20410151baa8a0037dfaa3c74a8e9'
        WHERE username = 'olena' AND password = 'secret456';
        """,
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE users
        SET password = 'secret123'
        WHERE username = 'andrii'
          AND password = 'pbkdf2_sha256$260000$060f7158b0fab874163bab919bef7dad$17299fd6f3252ff2295c86a5752b77f4c85c1617567842890e34f9659855a53b';
        """,
    )
    op.alter_column(
        "users",
        "password",
        existing_type=sa.String(length=255),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.execute(
        """
        UPDATE users
        SET password = 'secret456'
        WHERE username = 'olena'
          AND password = 'pbkdf2_sha256$260000$667e887685f3ca4913fd1c3221508ece$8b9f8d55c8892d1ffacdf7caeb7450b6e5e20410151baa8a0037dfaa3c74a8e9';
        """,
    )
