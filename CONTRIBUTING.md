# Sviluppo

È possibile compilare l'immagine tramite [docker cli](https://www.docker.com/) o [Visual Studio Code](https://code.visualstudio.com/), se volete debuggure il codice consiglio la seconda.

### Docker CLI
Per cotruire il container:
```bash
docker build -t mainkronos/anime_downloader .
```
- ⚠️ Il flag `-t` indica il tag del container.
- ⚠️ Il `.` NON è un errore di battitura, serve per indicare che il file `dockerfile` che contiene le istruzioni di compilazione si trova della directory corrente.

Per avviare:
```
docker run -d \
    --name=AnimeDownloader \
    -v /path/to/data:/script/json/ \
    -v /path/to/animeSeries:/tv \
    -v /path/to/downloads:/downloads \
    -v /path/to/connections:/script/connections \
    -p {port}:5000 \
    --env SONARR_URL=http://{url}:{port} \
    --env API_KEY=1234567890abcdefghijklmn \
    --env TZ=Europe/Rome \
    mainkronos/anime_downloader
```
- ⚠️ L'ultima riga deve COINCIDERE con il tag (inserito con il flag `-t`) usato al comando precedente.

### Visual Studio Code
Aprire la cartella del progetto in Visual Studio Code e modificate a vostro piacere il file [`tasks.json`](.vscode/tasks.json)

- Per modificare i valori delle variabili d'ambiente cambiate [questi valori](.vscode/tasks.json#L16-L20)
- Per modificare la porta esterna del container cambiate [questo valore](.vscode/tasks.json#L25)
- Per modificare i volumi cambiate [questi valori](.vscode/tasks.json#L29-L36)

E per avviare -> In Visual Studio Code -> `Esegui` -> `Avvia debug`.
