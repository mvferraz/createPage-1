import psycopg2
import os

print(os.environ.get('LOGGING_LEVEL'))


def connect_postgres():
    a = []
    conn = psycopg2.connect(
                            host=os.environ.get('POSTGRES_DB_HOST'),
                            database=os.environ.get('POSTGRES_DB_DATABASE'),
                            user=os.environ.get('POSTGRES_DB_USER'),
                            password=os.environ.get('POSTGRES_DB_PASSWORD')
                            )

    cur = conn.cursor()

    cur.execute('SELECT version()')

    cur.execute('select * from public.device_status')
    records = cur.fetchall()

    for record in records:
        a.append(record)
        print(record)

    cur.close()
    conn.close()
    return a

