"""fix timestamp with no tz in address and user

Revision ID: f9a075aca5a0
Revises: 7910ea212366
Create Date: 2024-06-06 07:53:53.723655

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f9a075aca5a0'
down_revision: Union[str, None] = '7910ea212366'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # change type of created_at and updated_at to datetime with timezone
    op.execute(
        """
        ALTER TABLE "user" ALTER COLUMN "created_at" TYPE timestamp with time zone;
        ALTER TABLE "user" ALTER COLUMN "updated_at" TYPE timestamp with time zone;
        ALTER TABLE "user" ALTER COLUMN "birthdate" TYPE timestamp with time zone;
        ALTER TABLE "address" ALTER COLUMN "updated_at" TYPE timestamp with time zone;
        """
    )
    pass


def downgrade() -> None:
    # change type of created_at and updated_at to datetime
    op.execute(
        """
        ALTER TABLE "user" ALTER COLUMN "created_at" TYPE timestamp;
        ALTER TABLE "user" ALTER COLUMN "updated_at" TYPE timestamp;
        ALTER TABLE "user" ALTER COLUMN "birthdate" TYPE timestamp;
        ALTER TABLE "address" ALTER COLUMN "updated_at" TYPE timestamp;
    """
    )
    pass
