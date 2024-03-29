from sqlalchemy import create_engine, select, MetaData, Table


def pg_auth():
    # to authorize my postgresql cluster in local machine
    engine = create_engine('postgresql://postgres:password@localhost:5432/xccelerated')

    return engine


def write_to_pg(dataframe, table_name: str):
    # a table is automatically created with given name and writes dataframe as postgres table
    dataframe.to_sql(table_name, pg_auth())


def read_from_pg(table_name: str):
    # used to copy a table in postgres to python

    metadata = MetaData(bind=None)
    table = Table(
        table_name,
        metadata,
        autoload=True,
        autoload_with=pg_auth()
    )

    temp_res = select([
        table.columns.median_num_session,
        table.columns.median_time
    ])

    connection = pg_auth().connect()
    results = connection.execute(temp_res).fetchall()

    return results
