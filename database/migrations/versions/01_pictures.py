"""pictures

Revision ID: 01
Revises: 
Create Date: 2024-05-26 13:35:17.001036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from database.utils import sql_importer


# revision identifiers, used by Alembic.
revision: str = '01'
down_revision: Union[str, None] = None
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
