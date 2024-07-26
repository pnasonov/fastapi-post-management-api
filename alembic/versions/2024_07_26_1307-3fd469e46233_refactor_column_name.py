"""refactor column name

Revision ID: 3fd469e46233
Revises: eeb8390253a3
Create Date: 2024-07-26 13:07:42.902832

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3fd469e46233"
down_revision: Union[str, None] = "eeb8390253a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "commentaries", sa.Column("is_blocked", sa.Boolean(), nullable=True)
    )
    op.drop_column("commentaries", "is_offensive")
    op.add_column(
        "posts", sa.Column("is_blocked", sa.Boolean(), nullable=True)
    )
    op.drop_column("posts", "is_offensive")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "posts", sa.Column("is_offensive", sa.BOOLEAN(), nullable=True)
    )
    op.drop_column("posts", "is_blocked")
    op.add_column(
        "commentaries", sa.Column("is_offensive", sa.BOOLEAN(), nullable=True)
    )
    op.drop_column("commentaries", "is_blocked")
    # ### end Alembic commands ###
