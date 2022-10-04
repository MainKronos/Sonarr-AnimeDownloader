
# ![wallpaper](/documentation/images/wallpaper.png)

<!-- [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)   [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)    -->

[![Version](https://img.shields.io/github/v/release/MainKronos/Sonarr-AnimeDownloader?color=90caf9&style=for-the-badge)](../../releases)   [![Issues](https://img.shields.io/github/issues/MainKronos/Sonarr-AnimeDownloader?color=a5d6a7&style=for-the-badge)](../../issues)   [![License](https://img.shields.io/github/license/MainKronos/Sonarr-AnimeDownloader?color=ffcc80&style=for-the-badge)](/LICENSE)   [![Stars](https://img.shields.io/github/stars/MainKronos/Sonarr-AnimeDownloader?color=fff59d&style=for-the-badge)](../../stargazers)

_This documentation is in **Italian** because this program downloads anime with italian subtitles only._

Questo Docker Container funziona come un'estenzione di [Sonarr](https://sonarr.tv/); serve a scaricare in automatico tutti gli anime che non vengono condivisi tramite torrent.
Il Container si interfaccia con Sonarr per avere informazini riguardante gli anime mancanti sull'hard-disk, viene poi fatta una ricerca se sono presenti sul sito [AnimeWorld](https://www.animeworld.tv/), e se ci sono li scarica e li posiziona nella cartella indicata da Sonarr.

L'utilizzo di _**Sonarr**_ è necessario.
Il _Docker Container_ di **Sonarr** può essere trovato [qui](https://github.com/linuxserver/docker-sonarr).

Il progetto utilizza la libreria `animeworld`, il codice sorgente e la documentazione è reperibile [qui](../../../AnimeWorld-API).

Le **FAQ** si trovano [qui](FAQ.md).

Se vuoi dare un'occhiata al progetto c'è una **DEMO** disponibile [_**qui**_](https://mainkronos.github.io/Sonarr-AnimeDownloader/). 👈(ﾟヮﾟ👈)

Se il progetto ti è _**piaciuto**_ e ti è stato _**utile**_, metti una <a href="https://github.com/MainKronos/Sonarr-AnimeDownloader/stargazers" style="font-weight:700;color:#9FA8DA;text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 0 0 25px rgba(255,255,0,0.3);">**STELLA**</a>.

![Presentazione](/documentation/images/Presentazione.gif)

## Utilizzo

Per avviare il container è possibile farlo attraverso _docker cli_ o tramite _docker-compose_.

### docker-compose ([clicca qui per maggiori informazioni](https://docs.linuxserver.io/general/docker-compose))

```yaml
version: '3.9'
services:
  mainkronos:
    container_name: AnimeDownloader
    volumes:
      - '/path/to/data:/script/json/'
      - '/path/to/animeSeries:/tv'
      - '/path/to/downloads:/downloads'
      - '/path/to/connections:/script/connections'
    ports:
      - '{port}:5000'
    environment:
      - 'SONARR_URL=http://{url}:{port}'
      - 'API_KEY=1234567890abcdefghijklmn'
      - 'TZ=Europe/Rome'
      - 'PUID=1000'
      - 'PGID=1000
    image: 'ghcr.io/mainkronos/anime_downloader:latest'
```


### docker cli ([clicca qui per maggiori informazioni](https://docs.docker.com/engine/reference/commandline/cli/))

```bash
docker run -d \
    --name=AnimeDownloader \
    -v /path/to/data:/script/json/ \
    -v /path/to/animeSeries:/tv \
    -v /path/to/downloads:/downloads \
    -v /path/to/connections:/script/connections \
    -p {port}:5000 \
    --env SONARR_URL='http://{url}:{port}' \
    --env API_KEY='1234567890abcdefghijklmn' \
    --env TZ=Europe/Rome \
    --env PUID=1000 \
    --env PGID=1000 \
    ghcr.io/mainkronos/anime_downloader:latest
```

## Parametri

Le immagini del Docker Container vengono configurate utilizzando i parametri passati in fase di esecuzione (come quelli sopra). Questi parametri sono separati da due punti e indicano rispettivamente `<esterno>:<interno>` al Container. Ad esempio, `-v /path/to/data:/script/json/` indica che la cartella nella posizione `/path/to/data` si trova in `/script/json/` all'interno del Container, quindi tutto il contento di `/path/to/data è anche` in `/script/json/` all'interno del Container.

Parametro | Necessario | Funzione
 :---: | :---: | :---
`--name` | :x: | Indica il nome del Container, può essere qualsiasi cosa
`-v /tv` | :heavy_check_mark: | Posizione della libreria Anime su disco, vedi sotto per ulteriori informazioni
`-v /script/json/` | :heavy_check_mark: | Contiene file di configurazione
`-v /downloads` | :x: | Cartella dove verranno scaricati tutti gli episodi (poi verranno spostati nella giusta cartella di destinazione)
`-v /script/connections` | :x: | Contiene file di configurazione per le [Connections](FAQ.md##come-si-usano-le-connections)
`-p {port}:5000` | :heavy_check_mark: | La porta per la pagina web
`--env SONARR_URL` | :heavy_check_mark: | Url di Sonarr es. http://localhost:8989
`--env API_KEY` | :heavy_check_mark: | Api key di sonarr, vedi sotto per ulteriori informazioni
`--env TZ` | :heavy_check_mark: | Specifica un fuso orario, è necessario per il corretto funzionamento del Container
`--env PUID` | :x: | Specifica UserID. Vedi sotto per maggiori informazioni
`--env PGID` | :x: | Specifica GroupID. Vedi sotto per maggiori informazioni

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
Ad esempio se su Sonarr la cartella tv è mappata così: `-v /path/to/tvseries:/tv` allora su anime_downloader sarà `-v /path/to/animeSeries:/tv`, oppure se è `-v /path/to/tvseries:/miatv/perf/miacartella` diventerà `-v /path/to/animeSeries:/miatv/perf/miacartella`...

### User / Group Identifiers
Quando si utilizzano i volumi (-v flag) possono sorgere dei problemi di autorizzazione tra il sistema operativo host e il contenitore, il problema può essere evitato specificando il `PUID` utente e il `PGID` di gruppo.

Assicurati che tutte le directory di volume sull'host siano di proprietà dello stesso utente che hai specificato e qualsiasi problema di autorizzazione svanirà come per magia.

In questo caso `PUID=1000` e `PGID=1000`, per trovare il tuo usa `id user` come di seguito:
```bash
$ id username
  uid=1000(dockeruser) gid=1000(dockeruser) groups=1000(dockeruser)
```

## Avvio

### table.json
Il programma, per funzionare, necessita di un file che si chiama `table.json`, si trova nella cartella `/script/json/` all'interno del Container. Questo file indica al programma a quale nome di AnimeWorld corrisponde il titolo della serie su Sonarr. Per esempio abbiamo che il titolo del nostro anime su AnimeWorld è `Sword Art Online 3: Alicization`, mentre su Sonarr è indicato come stagione 3 di `Sword Art Online`, tale informazione deve essere formattata (come mostrato qui sotto) e inserita nel file `table.json` in modo tale che il programma riesca a capire dove andare a cercare gli episodi su AnimeWorld.

**È altamente consigliato usare la _pagina web_ alla porta `5000` per l'inserimento di queste informazioni.**

![Tabella Di Conversione](/documentation/images/add_anime.gif)

In ogni caso la formattazione di come sono inserite le informazioni nel file `table.json` sono riportate quà sotto, sottoforma di esempio:
```
[
    ...
    {   
        "absolute": false,
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

La struttura interna del Container è così strutturata:
```
/
 ├── downloads                 ### Cartella di download
 ├── script
 │   ├── app                   ### Pagina Web
 │   │   ├── ...
 │   │  ...
 │   ├── anime_downloader      ### Programma principale
 │   │   ├── ...
 │   │  ...
 │   ├── json
 │   │    ├── settings.json    ### Impostazioni
 │   │    └── table.json       ### Tabella di conversione
 │  ...                        ### Altri file utili
... 
```

## Settings

![Settings](/documentation/images/settings.png)

Parametro | Descrizione
 :---: | :---
**Livello del Log** | Indica quale tipo di messaggi mostrare nei log. Sconsiglio fortemente di impostare un livello superiore a `INFO`.
**Rinomina Episodi** | Indica se gli episodi devono essere rinominati secondo la formattazione impostata su *Sonarr* (`http://sonarr-url/settings/mediamanagement` in `Episode Naming`).
**Sposta Episodi** | Indica se gli episodi devono essere spostati nella cartella indicata da *Sonarr* oppure lasciarli nella cartella interna al container (`/downloads`).
**Intervallo Scan** | Indica quanto tempo deve passare (in minuti) tra una ricerca degli episodi mancanti e un'altra, e in caso di risultati il download.
**Auto Ricerca Link** | **!!!MODALITÀ SPERIMENTALE!!!** Ricerca automaticamente i link che non sono presenti nella tabella di conversione.

Le impostazioni si trovano in `http://localhost:5000/settings`

## Problemi
In caso di problemi o errori controllare prima di tutto i log del Container, di solito lì è indicato il problema; altrimenti segnalarlo su GitHub in questo repository sotto la sezione _Issues_.

### **Importante**
Se visualizzate questo tipo di errore:
```
🅰🅻🅴🆁🆃: Il sito è cambiato, di conseguenza la libreria è DEPRECATA.
```
Segnalatelo il prima possibile sotto la sezione _Issues_, in modo tale che possa risolverlo al più presto.

## FAQ
Le _*frequently asked questions*_ si trovano [qui](FAQ.md).

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=MainKronos/Sonarr-AnimeDownloader&type=Date)
