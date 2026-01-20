import redis
import hashlib
import os
import socket
from datetime import datetime

r = redis.Redis(host='redis', port=6379, decode_responses=True)
worker_id = socket.gethostname()

r.rpush('ready_list', worker_id)

print(f"worker {worker_id}: gotowy", flush=True)

while True:
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

                print(f"{worker_id}: Zapisuję wynik do cache'{i}'", flush=True)
                r.set('found_password', i)

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