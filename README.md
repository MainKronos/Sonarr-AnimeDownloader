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
`--env ANIME_PATH` | :heavy_check_mark: | Indica la posizione della cartella interna al Contaier di dove si trovano gli anime, vedi sotto per ulteriori informazioni
`--env SONARR_URL` | :heavy_check_mark: | Url di Sonarr es. http://localhost:8989
`--env API_KEY` | :heavy_check_mark: | Api key di sonarr, vedi sotto per ulteriori informazioni
`--env CHAT_ID` | :heavy_multiplication_x: | Chat ID di telegram, vedi sotto per ulteriori informazioni
`--env BOT_TOKEN` | :heavy_multiplication_x: | Token per il Bot di telegram, vedi sotto per ulteriori informazioni
`--env TZ` | :heavy_check_mark: | Specifica un fuso orario, è necessario per il corretto funzionamento del Container

### ANIME_PATH e /tv
Questa variabile serve per impostare la posizione della cartella degli anime anche quando la cartella ha un nome diverso per Sonarr.
Per esempio abbiamo che nel nostro Container la cartella degli anime si trovi in `/tv/Anime/` mentre nel container di sonarr la stessa cartella è stata definita nella posizione `/tv/SerieTV/Anime/`, è di vitale importanza per il corretto funzionamento del Container che la variabile d'ambiente ANIME_PATH venga impostata a `/tv/Anime/`.
Nel caso in cui il parametro `-v /tv` si diverso e necessario modificare anche la variabile ANIME_PATH, per esempio se il parametro è `-v /Serie/tv2/` allora la variabile ANIME_PATH sarà `/Serie/tv2/Anime/`.

La vostra cartella `Anime` può avere un nome diverso, questa cartella sarebbe la directory principale che contiene tutte le cartelle degli anime. Per esempio l'episodio 1 di un anime che si chiama `myAnime1` si troverà `/tv/Anime/myAnime1/S01E01.mp4`

## Avvio


## FAQ

### Dove posso reperire la chiave api di sonarr?
![Sonarr API KEY](/documentation/images/Sonarr_ApiKey.png)

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
	- [ ] Spiegare come funziona il table.json