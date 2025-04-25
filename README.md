# Eventhub

**Eventhub** er en nettside for arrangementer – enten du vil delta eller arrangere selv.  
Utforsk publiserte eventer, meld deg på det som interesserer deg, eller opprett ditt eget!

---

## Kom i gang

Følg stegene under for å sette opp prosjektet lokalt:

1. **Opprett miljøfil**  
   Lag en `.env`-fil ved å kopiere `.env.example`, og fyll inn din egen informasjon.

2. **Opprett databasen**  
   Åpne `create.sql` i MySQL Workbench og kjør scriptet for å opprette databasen.

3. **Generer testdata**  
   Kjør `fake_integrated.py` for å fylle tabellene med tilfeldig generert testdata.

   ```python
   python fake_integrated.py

   ```

4. **Start applikasjonen**  
   Kjør `app.py`, og åpne lenken som vises i terminalen for å bruke nettsiden.

   ```python
   python app.py
   ```

---
