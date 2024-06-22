"""create documents table

Revision ID: 138b7b24c945
Revises: 
Create Date: 2024-06-09 17:03:36.729286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '138b7b24c945'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('unique_name', sa.String(length=150), nullable=False),
        sa.Column('path', sa.String(length=150), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('path')
    )


def downgrade() -> None:
    op.drop_table('documents')
