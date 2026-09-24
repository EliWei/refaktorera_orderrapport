# Kodgranskning av order_report.py

## Utgångsläge
Scriptet går att köra och skapar fyra csv filer med försäljningsinfo.

## Granskningsfynd

### Fynd 1 - Flera ansvar är sammanblandade

**Observation:** Samma kodblock läser filen, bearbetar datan och sparar resultatet. Skriptet innehåller inga funktioner.

**Konsekvens:** Delarna blir svåra att testa var för sig, eftersom det inte finns några funktioner att anropa och varje test även behöver använda filsystemet.

**Förslag:** Separera filinläsning, transformationslogik och sparande i egna funktioner, t.ex. `load_data()`, `clean_data()`, `calculate_metrics()` och `save_results()`.

### Fynd 2 - Programmet körs på modulnivå

**Observation:** Hela arbetsflödet körs på modulnivå, direkt när filen laddas, eftersom det saknas `if __name__ == "__main__":`.

**Konsekvens:** Att importera filen läser och skriver filer. Koden får oväntade sidoeffekter och blir svår att återanvända i andra program.

**Förslag:** Lägg programstarten i en `main()`-funktion och skydda anropet med en main-guard.

### Fynd 3 - Valideringen ger ett generellt fel

**Observation:** Valideringen kastar `Exception` med det ospecifika meddelandet `Fel data`.

**Konsekvens:** Felet är svårt att felsöka, eftersom det inte framgår vilka kolumner som saknas. Det är också svårt att kontrollera specifikt i ett automatiskt test, eftersom `Exception` är för generell.

**Förslag:** Kasta ett `ValueError` med ett meddelande som listar de saknade kolumnerna, t.ex. genom att beräkna `required - set(data.columns)`.

### Fynd 4 - Ett generellt except döljer alla fel

**Observation:** Hela programmet ligger i ett enda `try`-block med `except Exception`, som skriver ut `Något gick fel:` följt av felmeddelandet.

**Konsekvens:** Alla typer av fel hanteras på samma sätt, oavsett om filen saknas, en kolumn är fel eller koden innehåller en bugg. Traceback visas inte, så det framgår inte vilken rad som orsakade felet. 

**Förslag:** Fånga specifika fel, t.ex. `FileNotFoundError` och `ValueError`, och logga dem med `logging.error()`. Logga oväntade fel med `logging.exception()`.

### Fynd 5 - Hårdkodade sökvägar och dold förutsättning om outputmappen

**Observation:** Sökvägen till indatafilen och outputmappen är hårdkodade och namnen på utfilerna står som textsträngar mitt i programflödet. Skriptet förutsätter att mappen `output` redan finns.

**Konsekvens:** Det går inte att köra programmet med andra filer utan att ändra i koden, och eftersom sökvägarna är relativa fungerar det bara om det körs från rätt katalog. Det blir också svårare att testa med tillfälliga sökvägar. 

**Förslag:** Samla sökvägarna i en liten konfiguration och låt sparfunktioner skapa målmappen vid behov.


### Fynd 6 - Statusmeddelanden använder print

**Observation:** `print()` används för att rapportera att programmet startar, hur många rader som lästs in, vilka filer som sparats och att körningen är klar.

**Konsekvens:** Det går inte att styra nivå, format eller destination för meddelandena. De går inte att filtrera efter loggnivå (t.ex. `INFO` mot `DEBUG`) och det framgår inte var meddelandet skapades.

**Förslag:** Byt ut `print()` mot `logging` med en logger per modul (`logging.getLogger(__name__)`) och konfigurera loggningen centralt via config.

### Fynd 7 - Namnen beskriver dataflödet dåligt

**Observation:** Namnen `result1` och `result2` är allmänna och säger väldigt lite om objektens innehåll eller roll.

**Konsekvens:** Dataflödet blir svårare att följa, särskillt om programmet skulle växa och fler mellanresultat skulle tillkomma.

**Förslag:** Använd beskrivande namn som följer filnamnen, t.ex. `sales_by_category` och `sales_by_region`.

### Fynd 8 - Koden är mer repetativ än den behöver vara

**Observation:** `result1`, `result2` och `returns_by_category` använder i stort sätt samma kod - den gruppera, aggregerar, räknar, sorterar och sparar. Det enda som skiljer är kolumnen som grupperas på och sorteringen.

**Konsekvens:** Koden blir onödigt lång.

**Förslag:** Skapa en funktion `summarise_by(data, column)` som grupperar, aggregerar och beräknar `return_rate`, och anropa den för `product_category` och `region`. 

### Fynd 9 - All kod låg i en enda fil

**Observation:** Hela programmet, konfiguration, inläsning, validering, bearbetning och sparande, låg i en och samma fil utan tydlig uppdelning mellan ansvarsområden.

**Konsekvens:** Det är svårt för en ny användare att snabbt hitta var i koden ett visst ansvar ligger, t.ex. var valideringen sker eller var filer sparas. Filen blir också svårare att navigera i ju mer den växer.

**Förslag:** Dela upp koden i ett paket med en modul per ansvarsområde, t.ex. `config.py`, `loading.py`, `validation.py`, `processing.py`, `reporting.py` och `main.py`, med `__main__.py` som körs via `python -m order_report` och `__init__.py`.

## Sammanfattning
Skriptet läser in orderdata och sparar fyra rapportfiler, men hela programflödet körs på modulnivå och blandar filhantering, transformation och sparning. 

## Prioritering

### Hög prioritet
1. Fynd 1 - Flera ansvar är sammanblandade
2. Fynd 2 - Programmet körs på modulnivå utan main-guard
3. Fynd 4 - Ett generellt except döljer alla fel
4. Fynd 9 - All kod ligger i en enda fil

### Medelprioritet
4. Fynd 3 - Valideringen ger ett generellt fel
5. Fynd 5 - Hårdkodade sökvägar och dold förutsättning om outputmappen
6. Fynd 6 - Statusmeddelanden använder print
7. Fynd 8 - Koden är mer repetitiv än den behöver vara

### Låg prioritet
8. Fynd 7 - Namnen beskriver dataflödet dåligt