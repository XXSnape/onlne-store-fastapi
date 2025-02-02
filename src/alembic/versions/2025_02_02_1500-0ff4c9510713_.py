"""empty message

Revision ID: 0ff4c9510713
Revises:
Create Date: 2025-02-02 15:00:16.558507

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0ff4c9510713"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("fullname", sa.String(), nullable=False),
        sa.Column(
            "email",
            sa.String(length=32),
            server_default="Неуказано",
            nullable=False,
        ),
        sa.Column(
            "phone",
            sa.String(length=32),
            server_default="Неуказано",
            nullable=False,
        ),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column(
            "is_admin", sa.Boolean(), server_default="0", nullable=False
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
