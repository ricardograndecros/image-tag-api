"""tags

Revision ID: 02
Revises: 01
Create Date: 2024-05-26 13:35:29.090279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from database.utils import sql_importer


# revision identifiers, used by Alembic.
revision: str = '02'
down_revision: Union[str, None] = '01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql = sql_importer.read_sql(revision_id=revision, context=op.get_context())
    op.execute(sa.DDL(
        sql
    ))


def downgrade() -> None:
    sql = sql_importer.read_sql(revision_id=revision, context=op.get_context(), downgrade=True)
    op.execute(sa.DDL(
        sql
    ))