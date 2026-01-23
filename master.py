import redis
import time
from pymongo import MongoClient

r = redis.Redis(host='redis', port=6379, decode_responses=True)
mongo_client = MongoClient('mongo', 27017)
collection = mongo_client.projekt_db.passwords

BATCH_SIZE = 1000
MAX_NUMBER = 100000
EXPECTED_WORKERS = 3

r.set("status_message", "Gotowy. Czekam na start.")

while True:
    while not r.exists("start_cmd"):
        time.sleep(0.5)

    target_hash = r.get("input_hash")
    r.delete("start_cmd")
    r.delete("found_signal")

    r.set("status_message", f"Przetwarzam hash: {target_hash[:6]}...")

    existing = collection.find_one({"hash": target_hash})
    if existing:
        r.set("status_message", f"Znaleziono w bazie: {existing['password']}")
        time.sleep(1)
        continue

    r.delete('tasks')
    if r.llen('ready_list') == 0:
        print("Brak workerów! Ale wrzucam zadania.")

    r.set("status_message", "Obliczenia w toku... Workery pracują.")

    for i in range(0, MAX_NUMBER, BATCH_SIZE):
        start = i
        end = i + BATCH_SIZE
        task = f"{start},{end},{target_hash}"
        r.lpush('tasks', task)

    while True:
        if r.exists("found_signal"):
            r.set("status_message", "SUKCES! Hasło odgadnięte.")
            break

        if r.llen('tasks') == 0:
            time.sleep(4)

            if r.exists("found_signal"):
                r.set("status_message", "SUKCES!")
            elif collection.find_one({"hash": target_hash}):
                r.set("status_message", "SUKCES! (Potwierdzono w bazie)")
                r.set("found_signal", "1")
            else:
                r.set("status_message", "NIE POWIODŁO SIĘ. Hasło poza zakresem.")
            break

        time.sleep(1)

    print("Koniec tury.")