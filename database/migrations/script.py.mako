"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from database.utils import sql_importer
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


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
