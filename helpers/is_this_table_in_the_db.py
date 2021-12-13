import psycopg2
from psycopg2.errors import UndefinedTable

from .env_vars import LOCAL_DB_URL


def get_query(query: str, uri: str = LOCAL_DB_URL):

    connection = psycopg2.connect(uri)
    cursor = connection.cursor()

    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def days_in_table(tablename: str = "raw_data.ais_2019") -> list:
    """ """
    existing_data = f"""
        select distinct basedatetime::date
        from {tablename}
    """

    try:
        result = get_query(existing_data)
        return sorted([str(x[0]) for x in result])
    except UndefinedTable:
        return []


if __name__ == "__main__":
    print(days_in_table())
