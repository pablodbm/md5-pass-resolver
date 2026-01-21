import redis
import hashlib
import os
import socket
from datetime import datetime
from pymongo import MongoClient

r = redis.Redis(host='redis', port=6379, decode_responses=True)
mongo_client = MongoClient('mongo', 27017)
collection = mongo_client.projekt_db.passwords
worker_id = socket.gethostname()

r.rpush('ready_list', worker_id)

print(f"worker {worker_id}: gotowy", flush=True)

while True:
    if r.exists("found_signal"):
        print(f"{worker_id}: Ktoś inny już znalazł hasło. Kończę pracę!", flush=True)
        break
    task = r.blpop('tasks', timeout=0)

    if task:
        data = task[1]
        parts = data.split(',')
        start = int(parts[0])
        end = int(parts[1])
        target = parts[2].strip()

        print(f"{worker_id}: Sprawdzam zakres {start}-{end}", flush=True)

        for i in range(start, end):
            hashed = hashlib.md5(str(i).encode()).hexdigest()

            if hashed == target:
                print(f"{worker_id}: Zapisuję wynik do MongoDB", flush=True)

                collection.insert_one({
                    "password": i,
                    "hash": target,
                    "worker_id": worker_id,
                    "found_at": datetime.now()
                })

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                report = (
                    f"Data: {timestamp}\n"
                    f"Znalazł: {worker_id}\n"
                    f"HASŁO: {i}\n"
                )
                try:
                    with open("/data/wynik.txt", "w") as f:
                        f.write(report)
                        f.flush()
                        os.fsync(f.fileno())
                except:
                    pass