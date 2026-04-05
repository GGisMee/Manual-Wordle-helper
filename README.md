## Wordle Solver & Filter

En rekursiv algoritm för att generera och filtrera möjliga 5-bokstavskombinationer baserat på Wordle-logik.

---

### 🛠 Funktioner
* **Logik-baserad generering:** Skapar ordkombinationer utifrån kända begränsningar (bokstäver som finns men är på fel plats).
* **Bokstavs-exkludering:** Filtrerar bort bokstäver som redan använts.
* **Språkmässig filtrering:** Rensar bort osannolika bokstavskombinationer med hjälp av Regex (t.ex. trippla vokaler eller ogiltiga starter som "jk-").

---

### Delar

1.  **Input:** Använda bokstäver + bokstäver med känd/okänd position.
2.  **Mapping:** Skapar en karta över möjliga platser per bokstav.
3.  **Rekursion (BFS):** Testar alla giltiga kombinationer.
4.  **Regex-filter:** Tar bort "skräpord" baserat på språkregler.


---

### Projektstruktur
* `main.py`: Huvudlogik och rekursiv sökning.
* `uncommon_neighbours.txt`: Lista med osannolika bokstavspar för filtrering.

---

### Användning
Justera `used` och `not_there` i `if __name__ == "__main__":` blocket:

```python
used = set("spirathwdmlj") # Bokstäver som är gråa
not_there = {1: "nyo", 2: "yeo", ...} # Gula bokstäver (position: bokstav)
```

Sedan kör:
`python main.py`
