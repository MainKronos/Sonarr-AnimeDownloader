
# ![wallpaper](docs/static/img/wallpaper.png)

<!-- [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)   [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)    -->

[![Version](https://img.shields.io/github/v/release/MainKronos/Sonarr-AnimeDownloader?color=90caf9&style=for-the-badge)](../../releases)   [![Issues](https://img.shields.io/github/issues/MainKronos/Sonarr-AnimeDownloader?color=a5d6a7&style=for-the-badge)](../../issues)   [![License](https://img.shields.io/github/license/MainKronos/Sonarr-AnimeDownloader?color=ffcc80&style=for-the-badge)](/LICENSE)   [![Stars](https://img.shields.io/github/stars/MainKronos/Sonarr-AnimeDownloader?color=fff59d&style=for-the-badge)](../../stargazers)

_This documentation is in **Italian** because this program downloads anime with italian subtitles only._

Questo Docker Container funziona come un'estenzione di [Sonarr](https://sonarr.tv/); serve a scaricare in automatico tutti gli anime che non vengono condivisi tramite torrent.
Il Container si interfaccia con Sonarr per avere informazini riguardante gli anime mancanti sull'hard-disk, viene poi fatta una ricerca se sono presenti sul sito [AnimeWorld](https://www.animeworld.so/), e se ci sono li scarica e li posiziona nella cartella indicata da Sonarr.

L'utilizzo di _**Sonarr**_ è necessario.
Il _Docker Container_ di **Sonarr** può essere trovato [qui](https://github.com/linuxserver/docker-sonarr).

Il progetto utilizza la libreria `animeworld`, il codice sorgente e la documentazione è reperibile [qui](../../../AnimeWorld-API).

## Installazione

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
      - 'port:5000'
    environment:
      - 'SONARR_URL=http://url:port'
      - 'API_KEY=1234567890abcdefghijklmn'
      - 'TZ=Europe/Rome'
      - 'PUID=1000'
      - 'PGID=1000'
    image: 'ghcr.io/mainkronos/anime_downloader:latest'
```

## [Documentazione](https://mainkronos.github.io/Sonarr-AnimeDownloader)

La documentaszione con tutte le informazioni di installazione e configurazione sono disponibili [qui](https://mainkronos.github.io/Sonarr-AnimeDownloader).

Per iniziare ad utilizzare il programma vai alla sezione [QuickStart](usage/quickstart.md).

Se vuoi saperne di più sulle funzionalità avanzate vai alla sezione [Advanced Usage](usage/advanced.md).

In caso di dubbi o problemi consolutare le [FAQ](usage/faq.md).

Se vuoi contribuire al progetto dai un occhiata alla sezione [Contributing](community/contributing.md).

Un esempio di interfaccia e funzionamento del programma:

![Presentazione](docs/static/img/Presentazione.gif)

Se il progetto ti è _**piaciuto**_ aggiungi una [**STELLA**](https://github.com/MainKronos/Sonarr-AnimeDownloader/stargazers). 👈(ﾟヮﾟ👈)

## Sponsor

> **Grazie di cuore a tutti coloro che hanno donato** per questo progetto. \
> Il vostro supporto mi ha permesso di raggiungere **risultati straordinari**.

[![sponsors](https://raw.githubusercontent.com/MainKronos/MainKronos/main/res/sponsors.svg)](https://github.com/sponsors/MainKronos)

## Star History

![Star History Chart](https://api.star-history.com/svg?repos=MainKronos/Sonarr-AnimeDownloader&type=Date)
