from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
import uuid
import time

# config
batch_num = 10
batch_size = 10_0000
cassandra_batch_size = 10

# CREATE KEYSPACE schema1 WITH replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
# USE schema1
def create_table(session) -> None:
    session.execute(
        """
        CREATE TABLE names (
            id varchar PRIMARY KEY,
            name varchar
        )
        """
    )


def insert_tuples(session) -> None:

    for batch_idx in range(0, batch_size * batch_num, cassandra_batch_size):

        insert_names = session.prepare('INSERT INTO names (id, name) VALUES (?, ?)')
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        for row_idx in range(cassandra_batch_size):
            try:
                uuid_str = str(uuid.uuid4())
                batch.add(insert_names, (str(row_idx), uuid_str))
                print(f'Row {batch_idx + row_idx} Inserted into the table')
            except Exception as e:
                print(f'The cassandra error: {e}')

        session.execute_async(batch)


if __name__ == '__main__':
    cluster = Cluster()
    session = cluster.connect("schema1")

    # create_table(session=session)

    start = time.time()
    insert_tuples(session=session)
    end = time.time()

    print(f"{end - start} seconds are taken to insert for {batch_num * batch_size / cassandra_batch_size} batches with batch_size as {cassandra_batch_size}.")

    # 55 seconds to insert 1 million rows with cassandra_batch_size = 1000
