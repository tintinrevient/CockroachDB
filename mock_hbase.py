import happybase
import uuid
import time


# config
batch_num = 10
batch_size = 10_0000

# start hbase service + thrift service - by default, the thrift service listens on port 9090
# start-hbase.sh
# hbase-daemon.sh start thrift

# hbase shell
# list
# disable "names"
# drop "names"
# scan "names"

# database setup
connection = happybase.Connection(host="0.0.0.0")
connection.open()

def create_table() -> None:
    connection.create_table(
        'names',
        {'cf1': dict(max_versions=10, block_cache_enabled=True)}
    )


def insert_tuples() -> None:
    table = connection.table("names")
    batch = table.batch(batch_size=batch_size)

    for _ in range(batch_size * batch_num):
        uuid_binary_str = str(uuid.uuid4()).encode()
        batch.put(uuid_binary_str, {b'cf1:name': uuid_binary_str})

    batch.send()


def fetch_one(table, row_key: str) -> None:
    row = table.row(row_key.encode())
    print(row[b'family:name'])


def fetch_many(table, row_key_1: str, row_key_2: str) -> None:
    for key, data in table.rows([row_key_1.encode(), row_key_2.encode()]):
        print(key, data)


def scan(table, row_str: str) -> None:
    for key, data in table.scan(row_prefix=row_str.encode()):
        print(key, data)


def delete(table, row_key: str) -> None:
    row = table.delete(row_key.encode())


if __name__ == '__main__':
    # 31 seconds (4 minutes) to insert 1 million rows
    create_table()

    start = time.time()
    insert_tuples()
    end = time.time()

    print(f"{end - start} seconds are taken to insert for {batch_num} batches with batch_size as {batch_size}.")


