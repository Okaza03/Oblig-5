# Eventhub

**Eventhub** er en moderne nettside for arrangementer – enten du vil delta eller arrangere selv.  
Utforsk publiserte eventer, meld deg på det som interesserer deg, eller opprett ditt eget – alt samlet på én brukervennlig plattform!

---

## Funksjoner

- Bla gjennom tilgjengelige arrangementer  
- Opprett, rediger og slett egne eventer  
- Se hvem som deltar  
- Meld deg på eller fjern påmelding til eventer  
- Innlogging og brukerautentisering  
- Last opp bilder til dine arrangementer  

---

## Kom i gang

Følg stegene under for å sette opp prosjektet lokalt:

### 1. Klon GitHub-repositoriet

```bash
git clone https://github.com/Okaza03/Oblig-5.git
cd Oblig-5
```

### 2. Opprett miljøfil

Lag en `.env`-fil ved å kopiere `.env.example` og fylle inn dine egne verdier:

```bash
cp .env.example .env
```

### 3. Opprett databasen

Åpne `create.sql` i MySQL Workbench og kjør scriptet for å sette opp databasen.

### 4. Fyll databasen med testdata

```bash
python fake_integrated.py
```

### 5. Start applikasjonen

```bash
python app.py
```

Åpne lenken som vises i terminalen – vanligvis `http://127.0.0.1:5000/`.

---

## Teknologier brukt

| Teknologi   | Beskrivelse                          |
|-------------|--------------------------------------|
| Python      | Backend-språk                        |
| Flask       | Mikro-nettrammeverk for Python       |
| MySQL       | Relasjonsdatabase                    |
| TailwindCSS | Moderne CSS-rammeverk                |
| Faker       | Bibliotek for falske testdata        |
| Flask-WTF   | Skjemaer og CSRF-beskyttelse         |

---

## Bidra

Pull requests er hjertelig velkommen!  
Dersom du finner feil eller har forslag til forbedringer, opprett gjerne en issue eller kontakt prosjektansvarlig.

---

## Lisens

Dette prosjektet er lisensiert under [MIT-lisensen](https://opensource.org/licenses/MIT).

---

Laget med ❤️ av [@Okaza03](https://github.com/Okaza03) [@Havard03](https://github.com/Havard03) [@Pybruh](https://github.com/Pybruh)
