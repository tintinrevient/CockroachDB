# pip install psycopg2
import psycopg2
import psycopg2.extras
import uuid
import time


# config
batch_num = 10
batch_size = 10_0000

# database setup
# cockroach start-single-node --insecure --listen-addr=localhost
# cockroach sql --insecure
conn = psycopg2.connect(
    host="localhost",
    port="26257",
    database="defaultdb",
    user="admin",
    password="admin"
)

conn.autocommit = False


def create_table(cursor) -> None:
    try:
        cursor.execute("DROP TABLE IF EXISTS names")
        cursor.execute("""CREATE TABLE names
                                (name varchar(100) PRIMARY KEY NOT NULL)""")
        conn.commit()
    except Exception as ex:
        conn.rollback()
        print(ex)


def insert_tuples(cursor) -> None:
    start = time.time()

    query = """
    INSERT INTO names (name)
    VALUES %s
    """

    for batch_idx in range(batch_num):
        tuples = []

        for row_idx in range(batch_size):
            tuples.append((str(uuid.uuid4()),))

        try:
            psycopg2.extras.execute_values(cursor, query, tuples)
            conn.commit()

        except Exception as ex:
            conn.rollback()
            print(ex)

        print(f"Batch {batch_idx + 1} has been inserted with {batch_size} tuples.")


    end = time.time()
    print(f"{end - start} seconds are taken to insert for {batch_num} batches with batch_size as {batch_size}.")


if __name__ == '__main__':
    # 242 seconds (4 minutes) to insert 1 million rows
    with conn.cursor() as cursor:
        create_table(cursor)
        insert_tuples(cursor)

    conn.close()
