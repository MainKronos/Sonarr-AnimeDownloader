# FAQ


|DOMANDE|
|:---|
|[Dove posso reperire la chiave api di sonarr?](#dove-posso-reperire-la-chiave-api-di-sonarr)|
|[Dove posso reperire la Chat ID di telegram?](#dove-posso-reperire-la-chat-id-di-telegram)|
|[Dove posso reperire il Token per il Bot di telegram?](#dove-posso-reperire-il-token-per-il-bot-di-telegram)|
|[Ho aggiornato alla nuova versione del container e adesso non funziona più nulla](#dove-posso-reperire-il-token-per-il-bot-di-telegram)|
|[Una stagione di Sonarr è composta da due stagioni di AnimeWorld](#una-stagione-di-sonarr-è-composta-da-due-stagioni-di-animeworld)|
|[AnimeWorld Segue una numerazione Assoluta degli episodi](#animeworld-segue-una-numerazione-assoluta-degli-episodi)|
|[Uso Sonarr, ma non con Docker, e non sò quale mount dovrei fare](#uso-sonarr-ma-non-con-docker-e-non-sò-quale-mount-dovrei-fare)|
|[Ho bisogno di fare più mount](#ho-bisogno-fare-di-più-mount)|
|[Uso Sonarr in ambiente Windows, come devo fare il mount?](#uso-sonarr-in-ambiente-windows-come-devo-fare-il-mount)|
---

## Dove posso reperire la chiave api di sonarr?
![Sonarr API KEY](/documentation/images/Sonarr_ApiKey.png)

## Dove posso reperire la Chat ID di telegram?
Prima di reperire la Chat ID è necessario aver già creato un Bot Telegram, e per farlo basta continuare a leggere [qui](#dove-posso-reperire-il-token-per-il-bot-di-telegram).

Dopo aver creato il bot Telegram, bisogna inviargli un messaggio di prova con scritto qualsiasi cosa, serve per attivare la chat.
Poi bisogna andare su questa 'pagina':
```
https://api.telegram.org/bot<YourBOTToken>/getUpdates
```
Lì ci saranno scritte un po' di informazioni tipo queste riportate sotto, la vostra Chat ID si trova lì da qualche parte :) :
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

## AnimeWorld Segue una numerazione Assoluta degli episodi 
Se AnimeWorld segue una numerazione Assoluta degli episodi, come ad esempio 'One Piece', selezionare nella pagina web, nel Modal per l'aggiunta di un anime, la checkbox `absolute`. Di conseguenza il campo `Season` deve essere vuoto.


![Esempio](/documentation/images/AbsoluteCheckbox.png)

Se tutto è stato inserito correttamente apparirà un toast tipo questo:


![Esempio](/documentation/images/Toast.png)

E nell'elenco delle serie si potrà riconoscere facilmente gli anime impostati con un ordinamento assoluto grazie ad una targhettina come questa:


![Esempio](/documentation/images/SeasonAbsolute.png)

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
