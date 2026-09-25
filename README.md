# Orderrapport

Ett program som läser orderdata från en CSV-fil, bearbetar den och skapar rapporter över försäljning och returer per produktkategori och region.

## Förberedelser

1. Skapa en virtuell miljö och aktivera den:
python3 -m venv .venv
source .venv/bin/activate

2. Installera beroenden:
pip install pandas pytest

## Köra programmet

Kör från projektroten:
python -m src.order_report

Programmet läser `data/orders.csv` och sparar fyra rapportfiler i `output/`: `overview.csv`, `sales_by_category.csv`, `sales_by_region.csv` och `returns_by_category.csv`.

## Köra testerna
python -m pytest


## Projektstruktur

data/
orders.csv         # Indata (tillhandahållen av kursen)

output/
overview.csv
sales_by_category.csv
sales_by_region.csv
returns_by_category.csv

src/order_report/
__init__.py         # Exponerar main()
__main__.py         # Körstartpunkt (python -m src.order_report)
config.py           # ReportConfig-dataclass med sökvägar
main.py             # main(), loggningskonfiguration, felhantering
loading.py          # Läser in CSV-filen
validation.py       # Kontrollerar att nödvändiga kolumner finns
processing.py       # Rensar data och beräknar rapporter
reporting.py        # Sparar resultaten till fil

tests/
test_processing.py  # Test av summarise_by
test_loading.py     # Test av validate_columns (edge case)

old/
order_report_original.py    #orginalkod (används ej)

code_review.md      # Kodgranskning av originalkoden
pyproject.toml      # Pytest-konfiguration


## Reflektion

**Vilka var de viktigaste problemen i originalkoden?**
Hela programmet låg i en fil utan funktioner, kördes direkt vid import, hade duplicerad grupperingslogik för kategori och region, och dolde alla fel bakom ett generellt `except Exception`.

**Vilka förändringar tycker du förbättrade programmet mest?**
Uppdelningen i funktioner och sedan i moduler, gjorde koden mycket lättare att följa. 

**Varför valde du den projektstruktur du använde?**
Jag ville öva mig på att sätta ihop ett paket med en modul per ansvarsområde (config, inläsning, validering, bearbetning, rapportering, och en __main__) .

**Var använde du OOP/dataclass och varför passade det där?**
`ReportConfig` är en `frozen` dataclass som samlar sökvägarna till indata och output. Ärligt talat 
så tänkte jag först intuitivt att ha denna som en funktion, men i och med kravet på att skapa en klass
så såg jag denna som ett bra sätt att uppfylla kravet!

**Vilka viktiga beteenden skyddar dina automatiska tester?**
Ett test kontrollerar att `summarise_by` grupperar och räknar ut `return_rate` korrekt för normal data. Ett annat kontrollerar att saknade kolumner ger ett tydligt `ValueError`.

**Vad var svårast?**
Att strukturera om koden så att jag använde min egen funktion `summarise_by` i stället för den upprepande koden i result1, result2 och returns_by_category. Det tog en stund att klura ut hur funktionen skulle se ut, och sedan tog det tid att strukturera om koden.
Och så måste jag lägga till att jag lärde mig kommandot git diff för den här uppgiften. Och jag 
har kört git diff output/ hur många gånger som helst för att se till att refaktoreringen inte
påverkar output. 

**Vad hade du velat förbättra ytterligare om du haft mer tid?**
Bland annat att göra sökvägarna konfigurerbara, samt fler tester som täcker fler av funktionerna i `processing.py`.