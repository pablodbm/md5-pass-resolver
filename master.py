import redis
import time
import sys

r = redis.Redis(host='redis', port=6379, decode_responses=True)
TARGET_HASH = "674f3c2c1a8a6f90461e8a66fb5550ba"  # Przykladowy hash dla liczby 5678
BATCH_SIZE = 1000
MAX_NUMBER = 10000
EXPECTED_WORKERS = 3

print("Najpierw próbujemy pobrać dane z cache jeśli mamy już to policzone z poprzednich iteracji")
cached_password = r.get('found_password')

if cached_password:
    print(f"\n==========================================")
    print(f"Pobrano z cache")
    print(f" hasło: {cached_password}")
    print(f"==========================================\n")
    sys.exit(0)
else:
    print("NIe udało się pobrać danych z cache")

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