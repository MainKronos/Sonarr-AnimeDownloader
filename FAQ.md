# FAQ


|DOMANDE|
|:---|
|[Dove posso reperire la chiave api di sonarr?](#dove-posso-reperire-la-chiave-api-di-sonarr)|
|[Dove posso reperire la Chat ID di telegram?](#dove-posso-reperire-la-chat-id-di-telegram)|
|[Dove posso reperire il Token per il Bot di telegram?](#dove-posso-reperire-il-token-per-il-bot-di-telegram)|
|[Ho aggiornato alla nuova versione del container e adesso non funziona più nulla](#dove-posso-reperire-il-token-per-il-bot-di-telegram)|
|[Una stagione di Sonarr è composta da due stagioni di AnimeWorld](#una-stagione-di-sonarr-è-composta-da-due-stagioni-di-animeworld)|
|[AnimeWorld Segue una numerazione Assoluta degli episodi](#animeworld-segue-una-numerazione-assoluta-degli-episodi)|
|[Devo cancellare/modificare un link/stagione/anime](#devo-cancellaremodificare-un-linkstagioneanime)|
|[Uso Sonarr, ma non con Docker, e non sò quale mount dovrei fare](#uso-sonarr-ma-non-con-docker-e-non-sò-quale-mount-dovrei-fare)|
|[Ho bisogno di fare più mount](#ho-bisogno-fare-di-più-mount)|
|[Uso Sonarr in ambiente Windows, come devo fare il mount?](#uso-sonarr-in-ambiente-windows-come-devo-fare-il-mount)|
|[Cosa significa che la serie è stata scartata per mancanza di informazioni?](#cosa-significa-che-la-serie-è-stata-scartata-per-mancanza-di-informazioni)|
|[La serie non compare nei log](#la-serie-non-compare-nei-log)|
|[Come si usano le Connections?](#come-si-usano-le-connections)|
|[Come si usano i Tag?](#come-si-usano-i-tag)|
|[Non trovo nessuna soluzione al mio problema](#non-trovo-nessuna-soluzione-al-mio-problema)|
---

## Dove posso reperire la chiave api di sonarr?
![Sonarr API KEY](/documentation/images/sonarr_api_key.png)

## Dove posso reperire la Chat ID di telegram?
Prima di reperire la Chat ID è necessario aver già creato un Bot Telegram, e per farlo basta continuare a leggere [qui](#dove-posso-reperire-il-token-per-il-bot-di-telegram).

Dopo aver creato il bot Telegram, bisogna inviargli un messaggio di prova con scritto qualsiasi cosa, serve per attivare la chat.
Poi bisogna andare su questa 'pagina':
```
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```
Lì ci saranno scritte un po' di informazioni tipo queste riportate sotto, la vostra Chat ID si trova lì da qualche parte:
```
{
    "ok":true,
    "result":[{
        "update_id":379225167,
        "message":{
            "message_id":5,
            "from":{
                "id":123456789,
                "first_name":"MyName",
                "language_code":"it-IT"
            },"chat":{
                "id":987654321,     <---------------------------------------------------- Chat ID
                "first_name":"MyName",
                "type":"private"
            },
            "date":123456,
            "text":"hello"
        }
    }]
}
```

## Dove posso reperire il Token per il Bot di telegram?
Per prima cosa bisogna creare il proprio bot Telegram e per farlo basta seguire [queste](https://core.telegram.org/bots#3-how-do-i-create-a-bot) istruzioni.
Il token verrà generato alla creazione del bot. Leggere [qui](https://core.telegram.org/bots#6-botfather) per ulteriori informazioni.

## Ho aggiornato alla nuova versione del container e adesso non funziona più nulla
Alcune volte faccio modifiche importanti al programma, se riscontrate questo tipo di problema per favore controllate il [changelog](../../releases).

## Una stagione di Sonarr è composta da due stagioni di AnimeWorld
![Esempio](/documentation/images/animewold_2_serie.png)

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
Per aggiungere un campo, in questo caso un nuovo link all'array, è sufficiente selezionare la stagione a cui corrispondono su Sonarr gli episodi da scaricare, e aggiungere il link relativo alla seconda/terza/... parte.

![Esempio](/documentation/images/add_2_link.png)

> **Note**
> Per ricordarti come configurare correttamente il programma in questi casi basta pensare che, il numero subito sotto il titolo dell'anime si riferisce alla stagione di Sonarr e i link sotto si riferiscono a dove si trovano gli episodi relativi a quella stagione.

Il problema è stato trattato [qui](https://github.com/MainKronos/Sonarr-AnimeDownloader/issues/93#issuecomment-1435927555).

## AnimeWorld Segue una numerazione Assoluta degli episodi 
Se AnimeWorld segue una numerazione Assoluta degli episodi, come ad esempio 'One Piece', selezionare nella pagina web, nel Modal per l'aggiunta di un anime, la checkbox `absolute`. Di conseguenza il campo `Season` deve essere vuoto.


![Esempio](/documentation/images/absolute_checkbox.png)

Se tutto è stato inserito correttamente apparirà un toast tipo questo:


![Esempio](/documentation/images/toast.png)

E nell'elenco delle serie si potrà riconoscere facilmente gli anime impostati con un ordinamento assoluto grazie ad una targhettina come questa:


![Esempio](/documentation/images/season_absolute.png)

## Devo cancellare/modificare un link/stagione/anime
È possibile cancellare o modificare link/stagione/anime presente nella tabella di conversione, per farlo è sufficiente premere tasto destro sull'elemento che si vuole modificare/cancellare e premere Edit/Delete.
Nel caso in cui si voglia modificare, dopo aver premuto Edit, apparirà un input dove si potrà inserire la modifica; per confermare la modifica bisogna premere il tasto `Enter` altrimenti per annularla premere il tasto `Escape`.
Se l'input perde il focus e non è stata rilevata nessuna modifica, l'input scomparirà automaticamente.

![Esempio](/documentation/images/edit_anime.gif)

## Uso Sonarr, ma non con Docker, e non sò quale mount dovrei fare
Se Sonarr non è installato tramite Docker, per riuscire a trovare la giusta cartella da collegare nel Container `Sonarr-AnimeDownloader` ti basta soltanto mantare le cartelle conteneti gli anime nella stessa posizione.
Ad esempio se hai la tua cartella degli anime nella posizione `/myfolder/myanime` il comando corretto sarà questo: `-v /myfolder/myanime:/myfolder/myanime`.
Il problema è stato trattato [qui](https://github.com/MainKronos/Sonarr-AnimeDownloader/issues/9#issuecomment-774676181).

## Ho bisogno fare di più mount
Se hai bisogno di fare più mount non c'è nessun problema basta però mantenere lo stesso schema delle cartelle gestite da Sonarr.
Ad esempio:
> Hai una parte degli anime si trovano su  `/myfolder/myanime`
> L'altra parte degli anime si trovano su  `/myfolder2/myanimeOther`  

La soluzione sarebbe di fare così:
```
-v /myfolder/myanime:/myfolder/myanime
-v /myfolder2/myanimeOther:/myfolder2/myanimeOther
```
Il problema è stato trattato [qui](https://github.com/MainKronos/Sonarr-AnimeDownloader/issues/9#issuecomment-774676181).

## Uso Sonarr in ambiente Windows, come devo fare il mount?
Non c'è problema se Sonarr è in esecuzione su Windows, basta solo prestare attenzione alle cartelle.
Ad esempio, abbiamo 3 cartelle da collegare:
```
H:\Anime2\
H:\FanSeries\
E:\Anime3\
```
La soluzione è fare in questo modo:
```
-v H:\Anime2\:/Anime2
-v H:\FanSeries\:/FanSeries
-v E:\Anime3\:/Anime3
```
Il problema è stato trattato [qui](https://github.com/MainKronos/Sonarr-AnimeDownloader/issues/9#issuecomment-774692933).

## Cosa significa che la serie è stata scartata per mancanza di informazioni?
Significa che quella stagione non ha ancora una numerazione assoluta su Sonarr.

## La serie non compare nei log

Se la serie non compare nei log controllare:

1) Che la tipologia della serie sia `anime`. ![serie_type](/documentation/images/serie_type.png)
2) Che l'url e l'API Key di Sonarr siano corretti.
3) Che la serie non sia stata esclusa a causa di qualche [tag](#come-si-usano-i-tag).

Se il problema è ancora presente allora aprire un issue.

Il problema è stato trattato [qui](https://github.com/MainKronos/Sonarr-AnimeDownloader/issues/46).

## Come si usano le Connections?

![connection](/documentation/images/connections.png)

Le connection sono Shell Script scritti in Bash che vengono eseguiti quando deve essere inviato un messaggio tramite un servizio esterno (tipo Telegram). Sono un po' meno user friendly ma altamente personalizzabili! Alcuni template possono essere trovati in questa [cartella](https://github.com/MainKronos/Sonarr-AnimeDownloader/tree/main/documentation/examples/connections).

Per utilizzarle è necessario prima scrive lo script in modo tale che possa ricevere un parametro ($1) che identifica il messaggio da inviare, poi salvare con estensione .sh e posizionarlo nella cartella /script/connections. Infine accedere alla pagina web, nella sezioni impostazioni, aggiungerlo e attivarlo.

![connection_howto](/documentation/images/connections_howto.gif)

## Come si usano i Tag?

![Tags](/documentation/images/tags.png)

Per aggiungere un nuovo tag basta premere il pulsante `+` e aggiungere un nome di un tag **già presente** su Sonarr. \
Per attivarne uno basta premere il pulsante in basso; se è visualizzato `ON` è attivo se invece è `OFF` è spento. \
Se viene visualizzata la scritta `Invalido` significa che quel tag è stato rimosso da Sonarr e quindi non è più valido (non può essere attivato).

Il funzionamento dei tag varia a seconda della modalità settata nelle impostazioni; può essere in modalità `BLACKLIST` (default) o `WHITELIST`, per maggiori informazioni gurdare nel README alla sezione [Settings](README.md#settings).

## Non trovo nessuna soluzione al mio problema

Se non hai trovato nessuna soluzione pertinente tra le FAQ, allora è possibile cercare tra gli issue se il problema è già stato trattato (guardare [qui](https://github.com/MainKronos/Sonarr-AnimeDownloader/issues?q=is%3Aissue+label%3A%22help+wanted%22%2Cquestion%2Cdocumentation+-label%3A%22fixed+on+dev%22))

Se ancora non hai trovato nessuna soluzione allora ti consiglio di aprire un issue (usare [questo template](https://github.com/MainKronos/Sonarr-AnimeDownloader/issues/new?assignees=MainKronos&labels=question&template=question.md&title=%5BQUESTION%5D+Titolo+domanda))