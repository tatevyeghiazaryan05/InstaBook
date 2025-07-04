"""Changed in enum

Revision ID: 1c7bfd34c6c3
Revises: 7b79ec1ba67c
Create Date: 2025-07-04 15:55:01.337353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c7bfd34c6c3'
down_revision: Union[str, Sequence[str], None] = '7b79ec1ba67c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa

# old enum and new enum
old_enum = sa.Enum('male', 'female', 'other', name='genderenum')
new_enum = sa.Enum('male', 'female', name='genderenum_new')

def upgrade():
    # 1. Create new enum type
    new_enum.create(op.get_bind(), checkfirst=False)

    # 2. Alter the column to use the new enum
    op.execute("ALTER TABLE users ALTER COLUMN gender TYPE genderenum_new USING gender::text::genderenum_new")

    # 3. Drop the old enum type
    op.execute("DROP TYPE genderenum")

    # 4. Rename the new enum to original name
    op.execute("ALTER TYPE genderenum_new RENAME TO genderenum")

def downgrade():
    # Recreate old enum with 'other'
    old_enum.create(op.get_bind(), checkfirst=False)
    op.execute("ALTER TABLE users ALTER COLUMN gender TYPE genderenum USING gender::text::genderenum")
    op.execute("DROP TYPE genderenum")
    op.execute("ALTER TYPE genderenum RENAME TO genderenum")
