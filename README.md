# Front-end k testovaču.

Webová aplikácia, ktorá bude obsahovať:
- databázu používateľov a skupín s rôznymi právami
- stránky na zobrazenie zadaní úloh, kôl a súťaží
- stránky na zobrazovanie výsledkov
- administrátorské rozhranie
- novinky / oznamy
- wiki / cms systém na písanie pravidiel a iných článkov
- dvojjazyčné prostredie
- ...

Komunikácia s testovačom a odovzdávanie úloh na testovanie bude vyriešené v samostatnej django-app.

## Spustenie

Treba odkomentovať `TESTOVAC_FRONT_SECRET_KEY` v `.env.prod`.
Získať `dump20221009.psql` a umiestniť ho na úroveň `Dockerfile`.

```bash
docker compose up -d --build
docker container start testovac-front-end-db-1

docker exec -it testovac-front-end-db-1 /bin/sh
# vnutri kontajneru
psql -U testovac testovac <dump.psql
exit

docker compose up
# a potom otvoriť http://localhost:1337
```
