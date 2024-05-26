import glob

from alembic.migration import MigrationContext

def read_sql(revision_id: str, context: MigrationContext, downgrade=False) -> str:
    """Receives a migration id. Looks for its corresponding
    schema migration .sql script and returns its content.

    Args:
        str: the revision_id being executed
    Returns:
        str: the content of the corresponding migration .sql script
    """
    print("Running migration for revision ", revision_id)
    database_path = '/'.join(context.config.get_main_option('script_location').split('/')[:-1])
    r_suffix = '.up.sql' if not downgrade else '.down.sql'
    r = database_path + '/schemas/' + revision_id + '*' + r_suffix
    schema_file = glob.glob(r)[0]
    with open(schema_file) as sf:
        sql_content = sf.read()
    return sql_content