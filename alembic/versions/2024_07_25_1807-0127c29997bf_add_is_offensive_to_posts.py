"""Add is_offensive to posts

Revision ID: 0127c29997bf
Revises: 2badaf72db4a
Create Date: 2024-07-25 18:07:38.511943

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0127c29997bf"
down_revision: Union[str, None] = "2badaf72db4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "posts", sa.Column("is_offensive", sa.Boolean(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "is_offensive")
    # ### end Alembic commands ###
