# Sonarr-AnimeDownloader

Questo Docker funziona come un'estenzione di [Sonarr](https://sonarr.tv/); serve a scaricare in automatico tutti gli anime che non vengono condivisi tramite torrent.
Il Docker si interfaccia con Sonarr per avere informazini riguardante gli anime mancanti sull'hard-disk, viene poi fatta una ricerca se sono presenti sul sito [AnimeWorld](https://www.animeworld.tv/), e se ci sono li scarica e li posiziona nella cartella indicata da Sonarr.
L'utilizzo di _**Sonarr**_ è necessario.

## Utilizzo

```
docker run -d \
	--name=AnimeDownloader \
	-v /path/to/data:/script/json/ \
	-v /path/to/animeSeries:/tv \
	--env ANIME_PATH="/path/to/animeSeriesLocal" \
	--env SONARR_URL='http://{url}:{port}' \
	--env API_KEY='{SonarrApi}' \
	--env CHAT_ID={TelegramChatID} \
	--env BOT_TOKEN='{TelegramBotToken}' \
	--env TZ=Europe/Rome \
	mainkronos/anime_downloader

```

## Parametri

Le immagini del Docker Container vengono configurate utilizzando i parametri passati in fase di esecuzione (come quelli sopra). Questi parametri sono separati da due punti e indicano rispettivamente `<esterno>:<interno>` al Container. Ad esempio, `-v /path/to/data:/script/json/` indica che la cartella nella posizione `/path/to/data` si trova in `/script/json/` all'interno del Container, quindi tutto il contento di `/path/to/data è anche` in `/script/json/ all'interno del Container`.

Parametro | Necessario | Funzione
 :------: | :--------: | :-------
`--name` | :heavy_multiplication_x: | Indica il nome del Container, può essere qualsiasi cosa
`-v /tv` | :heavy_check_mark: | Posizione della libreria Anime su disco
`-v /script/json/` | :heavy_check_mark: | Contiene file di configurazione
`--env ANIME_PATH` | :heavy_check_mark: | Indica la posizione della cartella interna al Contaier di dove si trovano gli anime
`--env SONARR_URL` | :heavy_check_mark: | Url di Sonarr es. http://localhost:8989
`--env API_KEY` | :heavy_check_mark: | Api key di sonarr, vedi sotto per ulteriori informazioni
`--env CHAT_ID` | :heavy_multiplication_x: | Chat ID di telegram, vedi sotto per ulteriori informazioni
`--env BOT_TOKEN` | :heavy_multiplication_x: | Token per il Bot di telegram, vedi sotto per ulteriori informazioni
`--env TZ` | :heavy_check_mark: | Specifica un fuso orario, è necessario per il corretto funzionamento del Container

## **FAQ**

### Dove posso reperire la chiave api di sonarr?
![Sonarr API KEY](/images/Sonarr_ApiKey.png)

### Dove posso reperire la Chat ID di telegram?
TODO: da fare

### Dove posso reperire il Token per il Bot di telegram?
TODO: da fare

## Roadmap

- [x] Creare una repository si GitHub
- [x] Creare un'immagine Docker su Docker Hub
- [ ] Fare una documentazione dettaglita
	- [x] Spiegare come reperire l'api key di sonarr
	- [ ] Spiegare come reperire la Chat Id di Telegram
	- [ ] Spiegare come reperire il Token del Bot Telegram