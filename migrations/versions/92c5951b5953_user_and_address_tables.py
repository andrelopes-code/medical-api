"""user_and_address_tables

Revision ID: 92c5951b5953
Revises:
Create Date: 2024-06-04 07:23:11.654299

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '92c5951b5953'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('email', sa.VARCHAR(length=255), nullable=False),
        sa.Column('gender', sa.Enum('male', 'female', 'other', name='usergender'), nullable=False),
        sa.Column('birthdate', sa.DateTime(), nullable=False),
        sa.Column(
            'user_type', sa.Enum('patient', 'doctor', 'admin', name='usertype'), nullable=True
        ),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('phone', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_table(
        'address',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('city', sa.VARCHAR(length=255), nullable=False),
        sa.Column('street', sa.VARCHAR(length=255), nullable=False),
        sa.Column('number', sa.VARCHAR(length=10), nullable=False),
        sa.Column('state', sa.VARCHAR(length=2), nullable=False),
        sa.Column('cep', sa.VARCHAR(length=9), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_address_cep'), 'address', ['cep'], unique=False)
    op.create_index(op.f('ix_address_city'), 'address', ['city'], unique=False)
    op.create_index(op.f('ix_address_number'), 'address', ['number'], unique=False)
    op.create_index(op.f('ix_address_state'), 'address', ['state'], unique=False)
    op.create_index(op.f('ix_address_street'), 'address', ['street'], unique=False)
    op.create_index(op.f('ix_address_user_id'), 'address', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_address_user_id'), table_name='address')
    op.drop_index(op.f('ix_address_street'), table_name='address')
    op.drop_index(op.f('ix_address_state'), table_name='address')
    op.drop_index(op.f('ix_address_number'), table_name='address')
    op.drop_index(op.f('ix_address_city'), table_name='address')
    op.drop_index(op.f('ix_address_cep'), table_name='address')
    op.drop_table('address')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.execute('DROP TYPE usergender')
    op.execute('DROP TYPE usertype')
    # ### end Alembic commands ###