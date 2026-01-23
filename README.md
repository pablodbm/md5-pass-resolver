# Projekt: Rozproszony łamacz haseł (Brute-force)

**Autor:** Paweł Słota 234025

---

Celem projektu jest zrobienie systemu znalezienie zakodowanego hasła md5 lecz z podziałem na workery aby przyśpieszyć wykonanie tego procesu

**Architektura:**
1.  master.py - steruje cały procesem, rozdziela zakresy według parametrów: BATCH_SIZE,MAX_NUMBER
2.  Redis - przekazuje zadania do workerów
4.  Mongo - trzymamy w niej już odgagnięte hasła jako cache
3.  worker.py - workery które pobierają zadania i sprawdzają podane zakresy - możemy uruchomić dowolną ilość
4. dashboard.py - frontend całej aplikacji z użyciem biblioteki streamlit 
---

##  Instrukcja uruchomienia

Uruchomienie od razu przeprowadza proces łamania hasła

1. Otwórz terminal w folderze projektu.
2. Wpisz komendę:
   ```bash
   docker-compose build
   docker compose up
3. Wejdź na stronę http://localhost:8501/ i wpisz dowolną liczbę zaszyfrowaną md5 z przedziału 1-100000 i poczekaj na odkodowanie   