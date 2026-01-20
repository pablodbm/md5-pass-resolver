# Projekt: Rozproszony łamacz haseł (Brute-force)

**Autor:** Paweł Słota 234025

---

Celem projektu jest zrobienie systemu znalezienie zakodowanego hasła md5 lecz z podziałem na workery aby przyśpieszyć wykonanie tego procesu

**Architektura:**
1 master.py - steruje cały procesem, rozdziela zakresy według parametrów: BATCH_SIZE,MAX_NUMBER
2 Redis - przekazuje zadania do workerów oraz służy za prosty cache do przetrzymywanie już znalezionych haseł
3 worker.py - workery które pobierają zadania i sprawdzają podane zakresy - możemy uruchomić dowolną ilość
---

##  Instrukcja uruchomienia

Uruchomienie od razu przeprowadza proces łamania hasła

1. Otwórz terminal w folderze projektu.
2. Wpisz komendę:
   ```bash
   docker-compose up --build