"""empty message

Revision ID: 8cc9ccc37896
Revises: 659c2f0e7a42
Create Date: 2025-02-07 20:50:53.771903

"""

from typing import Sequence, Union

import fastapi_storages.integrations.sqlalchemy
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8cc9ccc37896"
down_revision: Union[str, None] = "659c2f0e7a42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("reviews_user_id_fkey", "reviews", type_="foreignkey")
    op.create_foreign_key(
        None, "reviews", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "reviews", type_="foreignkey")
    op.create_foreign_key(
        "reviews_user_id_fkey",
        "reviews",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    # ### end Alembic commands ###
