# Idealo Preistracker Discord-Bot

Ein Discord-Bot zum automatischen Tracken von Produkten auf [Idealo](https://www.idealo.de/).  
Der Bot sendet Alerts in einen Discord-Channel, sobald ein Produkt den von dir festgelegten Zielpreis erreicht oder unterschreitet.

---

## **Features**

- `!track <Produkt-URL> <Zielpreis>` – Produkt zum Tracking hinzufügen  
- `!list` – Alle gespeicherten Produkte anzeigen  
- `!remove <ID>` – Produkt anhand ID löschen  
- Automatischer Preis-Checker im Hintergrund  
- Alerts direkt im Discord-Channel  
- Async HTTP-Requests via `aiohttp` für reibungsloses Tracking  
