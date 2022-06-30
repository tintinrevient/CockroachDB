# pip install psycopg2
import psycopg2
import psycopg2.extras
from psycopg2 import pool
import uuid
import time
import concurrent.futures


# config
batch_num = 10
batch_size = 10_0000

# database setup
# cockroach start-single-node --insecure --listen-addr=localhost
# cockroach sql --insecure
pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=10,
    maxconn=40,
    host="localhost",
    port="26257",
    database="defaultdb",
    user="admin",
    password="admin"
)


def create_table() -> None:
    conn = pool.getconn()
    cursor = conn.cursor()

    try:
        cursor.execute("DROP TABLE IF EXISTS names")
        cursor.execute("""CREATE TABLE names
                                (name varchar(100) PRIMARY KEY NOT NULL)""")
        conn.commit()
    except Exception as ex:
        conn.rollback()
        print(ex)
    finally:
        cursor.close()
        pool.putconn(conn)


def insert_tuples(batch_idx) -> None:
    conn = pool.getconn()
    cursor = conn.cursor()

    query = """
    INSERT INTO names (name)
    VALUES %s
    """

    tuples = []
    for row_idx in range(batch_size):
        tuples.append((str(uuid.uuid4()),))

    try:
        psycopg2.extras.execute_values(cursor, query, tuples)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        print(ex)
    finally:
        cursor.close()
        pool.putconn(conn)

    print(f"The batch {batch_idx} has been inserted with {batch_size} tuples.")


if __name__ == '__main__':
    # 204 seconds (4 minutes) to insert 1 million rows
    create_table()

    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(insert_tuples, batch_idx) for batch_idx in range(batch_num)]
        concurrent.futures.wait(futures)

    end = time.time()
    print(f"{end - start} seconds are taken to insert for {batch_num} batches with batch_size as {batch_size}.")

    pool.closeall()