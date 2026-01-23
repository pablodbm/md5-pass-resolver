import streamlit as st
import redis
from pymongo import MongoClient
import pandas as pd
import time

st.set_page_config(page_title="MD5 Cracker", layout="wide")
st.title("Distributed Password Cracker")

try:
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    mongo_client = MongoClient('mongo', 27017)
    collection = mongo_client.projekt_db.passwords
    db_status = "Online"
except:
    db_status = "Offline"

st.sidebar.header(f"Status bazy: {db_status}")

st.header("1. Zadaj hasło do złamania")

user_hash = st.text_input("Wklej hash MD5 z przedziału 1 - 100000:", value="674f3c2c1a8a6f90461e8a66fb5550ba")
st.caption("Przykładowy hash to liczba '5678'.")

status_msg = r.get("status_message") or "Gotowy"
is_busy = "Obliczenia" in status_msg or "Szukam" in status_msg or "Przetwarzam" in status_msg

c1, c2 = st.columns([1, 3])

with c1:
    if st.button("ROZPOCZNIJ ŁAMANIE", key="start_btn", type="primary", use_container_width=True, disabled=is_busy):
        r.set("input_hash", user_hash.strip())
        r.set("start_cmd", "1")
        st.success("Zlecenie wysłane!")
        time.sleep(0.5)
        st.rerun()

with c2:
    status_placeholder = st.empty()

st.divider()
metrics_placeholder = st.empty()

while True:
    current_status_msg = r.get("status_message") or "Gotowy"
    current_is_busy = "Obliczenia" in current_status_msg or "Szukam" in current_status_msg or "Przetwarzam" in current_status_msg

    with status_placeholder.container():
        if "SUKCES" in current_status_msg or "Znaleziono" in current_status_msg:
            st.success(f"**{current_status_msg}**")
        elif "NIE POWIODŁO" in current_status_msg:
            st.error(f"**{current_status_msg}**")
        elif current_is_busy:
            st.warning(f"⏳ **{current_status_msg}**")
        else:
            st.info(f"ℹ️ {current_status_msg}")

    with metrics_placeholder.container():
        try:
            queue_len = r.llen('tasks')
            ready_workers = r.llen('ready_list')
        except:
            queue_len = 0
            ready_workers = 0

        k1, k2, k3 = st.columns(3)
        k1.metric("Zadania w kolejce", queue_len)
        k2.metric("Aktywne Workery", ready_workers)

        cursor = collection.find({}, {"_id": 0, "password": 1, "hash": 1, "worker_id": 1, "found_at": 1})
        df = pd.DataFrame(list(cursor))
        k3.metric("Baza znalezionych haseł", len(df))

        st.subheader("Historia złamanych haseł")
        if not df.empty:
            df['found_at'] = pd.to_datetime(df['found_at'])
            st.dataframe(df.sort_values(by='found_at', ascending=False), use_container_width=True)
        else:
            st.write("Brak wyników w bazie.")

    if is_busy and not current_is_busy:
        time.sleep(2)
        st.rerun()

    time.sleep(1)