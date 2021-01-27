
![wallpaper](/documentation/images/wallpaper.jpg)
# Sonarr-AnimeDownloader

<!-- [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)   [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)    -->

[![Version](https://img.shields.io/github/v/release/MainKronos/Sonarr-AnimeDownloader?color=90caf9&style=for-the-badge)](../../releases)    [![Docker](https://img.shields.io/docker/image-size/mainkronos/anime_downloader?color=9fa8da&style=for-the-badge)](https://hub.docker.com/repository/docker/mainkronos/anime_downloader)   [![Issues](https://img.shields.io/github/issues/MainKronos/Sonarr-AnimeDownloader?color=a5d6a7&style=for-the-badge)](../../issues)   [![License](https://img.shields.io/github/license/MainKronos/Sonarr-AnimeDownloader?color=ffcc80&style=for-the-badge)](/LICENSE)   [![Stars](https://img.shields.io/github/stars/MainKronos/Sonarr-AnimeDownloader?color=fff59d&style=for-the-badge)](../../stargazers)

_This documentation is in **Italian** because this program downloads anime with subtitles in Italian only._

Questo Docker Container funziona come un'estenzione di [Sonarr](https://sonarr.tv/); serve a scaricare in automatico tutti gli anime che non vengono condivisi tramite torrent.
Il Container si interfaccia con Sonarr per avere informazini riguardante gli anime mancanti sull'hard-disk, viene poi fatta una ricerca se sono presenti sul sito [AnimeWorld](https://www.animeworld.tv/), e se ci sono li scarica e li posiziona nella cartella indicata da Sonarr.

L'utilizzo di _**Sonarr**_ è necessario.
Il _Docker Container_ di **Sonarr** può essere trovato [qui](https://github.com/linuxserver/docker-sonarr)

Il progetto utilizza la libreria `animeworld`, l'ho dovuta rendere **privata** perchè gli sviluppatori di [AnimeWorld](https://www.animeworld.tv/) non volevano che fosse pubblica. Se volete l'accesso scrivete [qui](../../issues/6)

![Presentazione](/documentation/images/Presentazione.gif)

## Utilizzo

```
docker run -d \
    --name=AnimeDownloader \
    -v /path/to/data:/script/json/ \
    -v /path/to/animeSeries:/tv \
    -p {port}:5000 \
    --env SONARR_URL='http://{url}:{port}' \
    --env API_KEY='1234567890abcdefghijklmn' \
    --env CHAT_ID=123456789 \
    --env BOT_TOKEN='123456789:ABCDEFGHIJKLM-abc_AbCdEfGhI12345678' \
    --env TZ=Europe/Rome \
    mainkronos/anime_downloader

```

## Parametri

Le immagini del Docker Container vengono configurate utilizzando i parametri passati in fase di esecuzione (come quelli sopra). Questi parametri sono separati da due punti e indicano rispettivamente `<esterno>:<interno>` al Container. Ad esempio, `-v /path/to/data:/script/json/` indica che la cartella nella posizione `/path/to/data` si trova in `/script/json/` all'interno del Container, quindi tutto il contento di `/path/to/data è anche` in `/script/json/` all'interno del Container.

Parametro | Necessario | Funzione
 :---: | :---: | :---
`--name` | :heavy_multiplication_x: | Indica il nome del Container, può essere qualsiasi cosa
`-v /tv` | :heavy_check_mark: | Posizione della libreria Anime su disco, vedi sotto per ulteriori informazioni
`-v /script/json/` | :heavy_check_mark: | Contiene file di configurazione
`-p {port}:5000` | :heavy_check_mark: | La porta per la pagina web
`--env SONARR_URL` | :heavy_check_mark: | Url di Sonarr es. http://localhost:8989
`--env API_KEY` | :heavy_check_mark: | Api key di sonarr, vedi sotto per ulteriori informazioni
`--env CHAT_ID` | :heavy_multiplication_x: | Chat ID di telegram, vedi sotto per ulteriori informazioni
`--env BOT_TOKEN` | :heavy_multiplication_x: | Token per il Bot di telegram, vedi sotto per ulteriori informazioni
`--env TZ` | :heavy_check_mark: | Specifica un fuso orario, è necessario per il corretto funzionamento del Container

### /tv
È importante, per il corretto funzionamento del container, che il volume legato alla directory `/tv` sia identico a quello usato per la configurazione di **Sonarr**.
Esempio
```
docker run -d \
  --name=sonarr \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/London \
  -p 8989:8989 \
  -v /path/to/data:/config \
  -v /path/to/tvseries:/tv \ <--------------------------------------------- IMPORTANTE
  -v /path/to/downloadclient-downloads:/downloads \
  --restart unless-stopped \
  ghcr.io/linuxserver/sonarr
```

## Avvio

### table.json
Il programma, per funzionare, necessita di un file che si chiama `table.json`, si trova nella cartella `/script/json/` all'interno del Container. Questo file indica al programma a quale nome di AnimeWorld corrisponde il titolo della serie su Sonarr. Per esempio abbiamo che il titolo del nostro anime su AnimeWorld è `Sword Art Online 3: Alicization`, mentre su Sonarr è indicato come stagione 3 di `Sword Art Online`, tale informazione deve essere formattata (come mostrato qui sotto) e inserita nel file `table.json` in modo tale che il programma riesca a capire dove andare a cercare gli episodi su AnimeWorld.

**È altamente consigliato usare la _pagina web_ alla porta `5000` per l'inserimento di queste informazioni.**
![Tabella Di Conversione](/documentation/images/tabella_di_conversione.gif)

Nella stessa cartella `/script/json/` c'è un programma scritto in python che si chiama **`tableEditor.py`** che facilita l'inserimento di tali informazioni, (in caso di eliminazioni accidentale il file può essere scaricato anche da [qui](/config/json/tableEditor.py)). Questo script deve essere nella **stessa** cartella di `table.json` altimenti non funzionerà correttamente.
**Dalla prossima versione il file non sarà più supportato.**
```
...
├── script
│   ├── app    ### Pagina Web
│   │   ├── ...
│   │  ...
│   ├── main.py    ### Programma principale
│   └── json
│       ├── table.json    ### Tabella di conversione
│       └── tableEditor.py
...        
```

In ogni caso la formattazione di come sono inserite le informazioni nel file `table.json` sono riportate quà sotto, sottoforma di esempio:
```
[
    ...
    {
        "title": "Sword Art Online",
        "seasons": {
            "1": [
                "https://www.animeworld.tv/play/sword-art-online.N0onT"
            ],
            "2": [
                "https://www.animeworld.tv/play/sword-art-online-2._NcG6"
            ]     
        }
    },
    ...
]
```
Ho caricato anche la **mia configurazione** che utilizzo, può essere trovata [qui](/documentation/examples/table.json). Questa `table.json` può essere usata come _esempio_ o come _prorio database_ da aggiornare poi personalmente con i propri **Anime**. Ad ogni stagione ne caricherò una più aggiornata. 

## Problemi
In caso di problemi o errori controllare prima di tutto i log del Container, di solito lì è indicato il problema; altrimenti segnalarlo su GitHub in questo repository sotto la sezione _Issues_.

## FAQ

### Dove posso reperire la chiave api di sonarr?
![Sonarr API KEY](/documentation/images/Sonarr_ApiKey.png)

### Dove posso reperire la Chat ID di telegram?
TODO: da fare

### Dove posso reperire il Token per il Bot di telegram?
TODO: da fare

### Ho aggiornato alla nuova versione del container e adesso non funziona più nulla.
Alcune volte faccio modifiche importanti al programma, se riscontrate questo tipo di problema per favore controllate il [changelog](releases).

### Una stagione di Sonarr comprende due stagioni su AnimeWorld
![Esempio](/documentation/images/AnimeWold_2serie.png)

Per riuscire a dire al programma che una stagione di Sonarr sono due di AnimeWold basta aggiunge all'Array dei link di AnimeWold per quella stagione di Sonarr anche il link di AnimeWold della seconda stagione.

Per l'esempio mostrato nell'immagine la sua formattazione nel `table.json` sarebbe:
```
[    
    ...
    {
        "title": "Ascendance of a Bookworm",
        "seasons": {
            "1": [
                "https://www.animeworld.tv/play/ascendance-of-a-bookworm.paCPb",
                "https://www.animeworld.tv/play/ascendance-of-a-bookworm-2.Q0Rrm"
            ]
        }
    },
    ...
]
```

**È altamente consigliato usare la _pagina web_ alla porta `5000` per l'inserimento di queste informazioni.**
Per aggiungere un campo, in questo caso un nuovo link all'array, e sufficiente reinserire tutti i campi (come se si stesse riaggiungendo di nuovo lo stesso anime) e nel campo link inserire **soltanto** il secondo/terzo/ecc. link. 


## Roadmap

- [x] Creare una repository su GitHub
- [x] Creare un'immagine Docker su Docker Hub
- [ ] Fare una documentazione dettaglita
    - [x] Spiegare come reperire l'`api key` di sonarr
    - [ ] Spiegare l'utilità e il funzionamento di un bot di telegram
        - [ ] Spiegare come reperire la `Chat Id` di Telegram
        - [ ] Spiegare come reperire il `Token` del Bot Telegram
    - [x] Spiegare come funziona il `table.json`
        - [x] Informazioni generali e funzionamento
        - [x] Funzionamento e utilizzo di `tableEditor.py`
        - [x] Come collegare più stagioni di AnimeWorld riferite a una di Sonarr
        - [x] Aggiungere un `table.json` di esempio
    - [x] Spiegare l'utilizzo della variabile ambientale `ANIME_PATH`
    - [x] Aggiungere i Providers supportati
