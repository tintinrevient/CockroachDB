import redis
import json
import uuid
import time


# config
batch_num = 10
batch_size = 10_0000

# start redis service
# brew services start redis
# redis-cli
redis_client = redis.Redis(host='localhost', port=6379, db=0, ssl=False)
pipe = redis_client.pipeline()

start = time.time()

for _ in range(batch_size * batch_num):
    uuid_str = str(uuid.uuid4())
    pipe.set(name=uuid_str, value=json.dumps({uuid_str: uuid_str}))

end = time.time()
print(f"{end - start} seconds are taken to insert for {batch_num} batches with batch_size as {batch_size}.")

set_response = pipe.execute()
# print("bulk insert response : ", set_response)

# 14 seconds to insert 1 million rows