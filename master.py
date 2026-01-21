import redis
import time
import sys
from pymongo import MongoClient

r = redis.Redis(host='redis', port=6379, decode_responses=True)
mongo_client = MongoClient('mongo', 27017)
collection = mongo_client.projekt_db.passwords

TARGET_HASH = "674f3c2c1a8a6f90461e8a66fb5550ba"
BATCH_SIZE = 1000
MAX_NUMBER = 10000
EXPECTED_WORKERS = 3

print("Sprawdzam bazę danych MongoDB")
existing_result = collection.find_one({"hash": TARGET_HASH})

if existing_result:
    print(f"\n==========================================")
    print(f"Pobrano z bazy danych")
    print(f" hasło: {existing_result['password']}")
    print(f"==========================================\n")
    sys.exit(0)
else:
    print("Brak wyniku w bazie danych")

r.delete('ready_list')
r.delete('tasks')

while True:
    ready_count = r.llen('ready_list')
    print(f"Gotowe workery: {ready_count}/{EXPECTED_WORKERS}")

    if ready_count >= EXPECTED_WORKERS:
        break
    time.sleep(1)

for i in range(0, MAX_NUMBER, BATCH_SIZE):
    start = i
    end = i + BATCH_SIZE
    task = f"{start},{end},{TARGET_HASH}"
    r.lpush('tasks', task)

print("Zadanie wysłane do workerów")