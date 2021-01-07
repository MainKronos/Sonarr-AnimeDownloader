![wallpaper](/documentation/images/wallpaper.jpg)
# Sonarr-AnimeDownloader

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)   [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

_This documentation is in **Italian** because this program downloads anime with subtitles in Italian only._

Questo Docker Container funziona come un'estenzione di [Sonarr](https://sonarr.tv/); serve a scaricare in automatico tutti gli anime che non vengono condivisi tramite torrent.
Il Container si interfaccia con Sonarr per avere informazini riguardante gli anime mancanti sull'hard-disk, viene poi fatta una ricerca se sono presenti sul sito [AnimeWorld](https://www.animeworld.tv/), e se ci sono li scarica e li posiziona nella cartella indicata da Sonarr.

L'utilizzo di _**Sonarr**_ è necessario.

Il _Docker Container_ di **Sonarr** può essere trovato [qui](https://github.com/linuxserver/docker-sonarr)

### Supported Providers

Gli episodi di AnimeWorld vengono caricati in altri siti, alcuni di loro (I più frequenti) sono supportati dal programma:

1. [YouTube](https://www.youtube.com/)
2. [VVVVID](https://www.vvvvid.it/show/1396/akudama-drive&r)
3. [Streamtape](https://streamtape.com/)
4. [AnimeWorld_Server](https://www.animeworld.tv/)

## AGGIORNAMENTI IMPORTANTI
```diff
- WARNING - WARNING - WARNING - 
```
**La nuova versione `0.3.0` ha una diversa formattazione del file `table.json`, per convertire la vecchia versione in quella nuova basta solo avviare il nuovo file `tableEditor.py`.**

Adesso è possibile aggiungere più stagioni di Sonarr riferite ad una di AnimeWorld (Funziona solo se la numerazione assoluta degli episodi di Sonarr combacia con quella di AnimeWorld).

## Utilizzo

```
docker run -d \
    --name=AnimeDownloader \
    -v /path/to/data:/script/json/ \
    -v /path/to/animeSeries:/tv \
    --env ANIME_PATH="/path/to/animeSeriesLocal" \
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
`-v /tv` | :heavy_check_mark: | Posizione della libreria Anime su disco
`-v /script/json/` | :heavy_check_mark: | Contiene file di configurazione
`--env ANIME_PATH` | :heavy_check_mark: | Indica la posizione della cartella interna al Container di dove si trovano gli anime, vedi sotto per ulteriori informazioni
`--env SONARR_URL` | :heavy_check_mark: | Url di Sonarr es. http://localhost:8989
`--env API_KEY` | :heavy_check_mark: | Api key di sonarr, vedi sotto per ulteriori informazioni
`--env CHAT_ID` | :heavy_multiplication_x: | Chat ID di telegram, vedi sotto per ulteriori informazioni
`--env BOT_TOKEN` | :heavy_multiplication_x: | Token per il Bot di telegram, vedi sotto per ulteriori informazioni
`--env TZ` | :heavy_check_mark: | Specifica un fuso orario, è necessario per il corretto funzionamento del Container

### ANIME_PATH e /tv
La variabile `ANIME_PATH` serve per impostare la posizione della cartella degli anime anche quando la cartella ha un nome diverso per Sonarr.
Per esempio abbiamo che nel nostro Container la cartella degli anime si trovi in `/tv/Anime/` mentre nel container di sonarr la stessa cartella è stata definita nella posizione `/tv/SerieTV/Anime/`, è di vitale importanza per il corretto funzionamento del Container che la variabile d'ambiente ANIME_PATH venga impostata a `/tv/Anime/`.
Nel caso in cui il parametro `-v /tv` sia diverso è necessario modificare anche la variabile ANIME_PATH, per esempio se il parametro è `-v /Serie/tv2/` allora la variabile ANIME_PATH sarà `/Serie/tv2/Anime/`.

La vostra cartella `Anime` può avere un nome diverso, questa cartella sarebbe la directory principale che contiene tutte le cartelle degli anime. Per esempio l'episodio 1 di un anime che si chiama `myAnime1` si troverà `/tv/Anime/myAnime1/S01E01.mp4`

```
tv
└── Anime
    ├── myAnime1
    │   ├── S01E01.mp4
    │   ├── S01E02.mp4
    │   ...
    ├── myAnime2
    │   ├── S01E01.mp4
    │   ├── S01E02.mp4
    │   ...
    ... 
            
```

## Avvio

### table.json
Il programma, per funzionare, necessita di un file che si chiama `table.json`, si trova nella cartella `/script/json/` all'interno del Container. Questo file indica al programma a quale nome di AnimeWorld corrisponde il titolo della serie su Sonarr. Per esempio abbiamo che il titolo del nostro anime su AnimeWorld è `Sword Art Online 3: Alicization`, mentre su Sonarr è indicato come stagione 3 di `Sword Art Online`, tale informazione deve essere formattata (come mostrato qui sotto) e inserita nel file `table.json` in modo tale che il programma riesca a capire dove andare a cercare gli episodi su AnimeWorld.

Nella stessa cartella `/script/json/` c'è un programma scritto in python che si chiama **`tableEditor.py`** che facilita l'inserimento di tali informazioni, (in caso di eliminazioni accidentale il file può essere scaricato anche da [qui](/config/json/tableEditor.py)). Questo script deve essere nella **stessa** cartella di `table.json` altimenti non funzionerà correttamente.
```
...
├── script
│   ├── main.py
│   └── json
│       ├── table.json
│       └── tableEditor.py
...        
```

In ogni caso la formattazione di come sono inserite le informazioni nel file `table.json` sono riportate quà sotto, sottoforma di esempio:
```
[
    ...
    {
        "Sonarr": {
            "title": "Sword Art Online",
            "season": [
                3
            ]
        },
        "AnimeWorld": {
            "title": [
                "Sword Art Online 3: Alicization"
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

### Una stagione di Sonarr comprende due stagioni su AnimeWorld
![Esempio](/documentation/images/AnimeWold_2serie.png)

Per riuscire a dire al programma che una stagione di Sonarr sono due di AnimeWold basta aggiunge all'Array del titolo di AnimeWold per quella stagione di Sonarr anche il titolo di AnimeWold della seconda stagione.

Per l'esempio mostrato nell'immagine la sua formattazione nel `table.json` sarebbe:
```
[    
    ...
    {
        "Sonarr": {
            "title": "Ascendance of a Bookworm",
            "season": [
                1
            ]
        },
        "AnimeWorld": {
            "title": [
                "Ascendance of a Bookworm",
                "Ascendance of a Bookworm 2"
            ]
        }
    },
    ...
]
```

Si può fare più comodamente anche con il `tableEditor.py` basta inserire:

```
Inserire titolo anime di Sonarr: Ascendance of a Bookworm
Inserire la stagione dell'anime Ascendance of a Bookworm: 1
Inserire titolo anime di AnimeWorld: Ascendance of a Bookworm
L'anime Ascendance of a Bookworm (stagione 1) è stato aggiunto correttamente.

---------------------------------------------

Inserire titolo anime di Sonarr: Ascendance of a Bookworm
Inserire la stagione dell'anime Ascendance of a Bookworm: 1
Inserire titolo anime di AnimeWorld: Ascendance of a Bookworm 2
L'anime Ascendance of a Bookworm (stagione 1) è gia presente, e corrisponde a ['Ascendance of a Bookworm']
Aggiungere il titolo Ascendance of a Bookworm 2 alla lista? (y/n): y

---------------------------------------------
```


## Roadmap

- [x] Creare una repository su GitHub
- [x] Creare un'immagine Docker su Docker Hub
- [ ] Fare una documentazione dettaglita
    - [x] Spiegare come reperire l'`api key` di sonarr
    - [ ] Spiegare l'utilità e il funzionamento di un bot di telegram
        - [ ] Spiegare come reperire la `Chat Id` di Telegram
        - [ ] Spiegare come reperire il `Token` del Bot Telegram
    - [ ] Spiegare come funziona il `table.json`
        - [x] Informazioni generali e funzionamento
        - [x] Funzionamento e utilizzo di `tableEditor.py`
        - [ ] Come collegare più stagioni di AnimeWorld riferite a una di Sonarr
        - [x] Aggiungere un `table.json` di esempio
    - [x] Spiegare l'utilizzo della variabile ambientale `ANIME_PATH`
    - [x] Aggiungere i Providers supportati
