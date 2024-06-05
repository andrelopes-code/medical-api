"""add_hashed_password_user_field

Revision ID: 4ba3bb48b7df
Revises: 92c5951b5953
Create Date: 2024-06-04 21:34:34.433503

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4ba3bb48b7df'
down_revision: Union[str, None] = '92c5951b5953'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.alter_column(
        'user',
        'user_type',
        existing_type=postgresql.ENUM('patient', 'doctor', 'admin', name='usertype'),
        nullable=False,
    )
    op.alter_column('user', 'phone', existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'phone', existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        'user',
        'user_type',
        existing_type=postgresql.ENUM('patient', 'doctor', 'admin', name='usertype'),
        nullable=True,
    )
    op.drop_column('user', 'hashed_password')
    # ### end Alembic commands ###
