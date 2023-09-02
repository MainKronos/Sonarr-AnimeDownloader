WARNC='\033[93m' #GIALLO
ALERTC='\033[91m' # ROSSO
ERRORC='\033[4;3;91m' # ROSSO
TITLEC='\033[1;94m' # BLU
SEPARC='\033[90m' # GRIGIO
DIVIDC='\033[1;90m' # GRIGIO
OKC='\033[92m' # VERDE
NC='\033[0m' # Ripristino


START_LOG = """\033[1;94m┌───────────────────────────────────[{time}]───────────────────────────────────┐
\033[1;94m│                 _                _____                      _                 _            │
\033[1;94m│     /\\         (_)              |  __ \\                    | |               | |           │
\033[1;94m│    /  \\   _ __  _ _ __ ___   ___| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __  │
\033[1;94m│   / /\\ \\ | '_ \\| | '_ ` _ \\ / _ \\ |  | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |/ _ \\ '__| │
\033[1;94m│  / ____ \\| | | | | | | | | |  __/ |__| | (_) \\ V  V /| | | | | (_) | (_| | (_| |  __/ |    │
\033[1;94m│ /_/    \\_\\_| |_|_|_| |_| |_|\\___|_____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\\___|_|    │
\033[1;94m│                                                                                            │
\033[1;94m└────────────────────────────────────{version:─^20}────────────────────────────────────┘\033[0m"""

SONARR_URL_ERROR_LOG = "✖️ Variabile d'ambinete '𝙎𝙊𝙉𝘼𝙍𝙍_𝙐𝙍𝙇' non inserita."
SONARR_URL_CHECK_LOG = "✔️ 𝙎𝙊𝙉𝘼𝙍𝙍_𝙐𝙍𝙇: {sonar_url}"

API_KEY_ERROR_LOG = "✖️ Variabile d'ambinete '𝘼𝙋𝙄_𝙆𝙀𝙔' non inserita."
API_KEY_CHECK_LOG = "✔️ 𝘼𝙋𝙄_𝙆𝙀𝙔: {api_key}"

SETTINGS_UPDATED_LOG = "✔️ impostazioni aggiornate correttamente."
SETTINGS_SCAN_DELAY_LOG = "⚙️ Intervallo Scan: {delay} minuti."
SETTINGS_RENAME_EPISODE_LOG = "⚙️ Rinomina Episodi: {status}."
SETTINGS_MOVE_EPISODE_LOG = "⚙️ Sposta Episodi: {status}."
SETTINGS_AUTO_BIND_LINK_LOG = "⚙️ Auto Ricerca Link: {status}."
SETTINGS_LOG_LEVEL_LOG = "⚙️ Livello del Log: {level}."
TAG_MODE_LOG = "⚙️ Modalità dei Tag: {mode}."


START_SERVER_LOG = "✔️ Server Avviato."

DIVIDER_LOG = "\033[1;90m─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ \033[0m"
SEPARATOR_LOG = "\033[1;90m──────────────────────────────────────────────────────────────────────────────────────────────\033[0m"
START_BLOCK_LOG = "\033[90m╭───────────────────────────────────「{time}」───────────────────────────────────╮\033[0m"
END_BLOCK_LOG = "\033[90m╰───────────────────────────────────「{time}」───────────────────────────────────╯\033[0m"

ANIME_REJECTED_LOG = "⁉️ Serie '{anime}' S{season} scartata per mancanza di informazioni."
ANIME_EXCLUDED_LOG = "🪧 Serie '{anime}' scartata per i tag."
EPISODE_REJECTED_LOG = "⁉️ Episodio '{anime}' S{season}E{episode} scartato per mancanza di numerazione assoluta."

CONNECTION_ERROR_LOG = "⚠️ Errore di connessione. ({res_error})"

LINK_INEXISTENT_LOG = "❌ Il link della 𝘴𝘵𝘢𝘨𝘪𝘰𝘯𝘦 {season} della 𝘴𝘦𝘳𝘪𝘦 '{anime}' non esiste nella 𝗧𝗮𝗯𝗲𝗹𝗹𝗮 𝗗𝗶 𝗖𝗼𝗻𝘃𝗲𝗿𝘀𝗶𝗼𝗻𝗲."
SEASON_INEXISTENT_LOG = "❌ La 𝘴𝘵𝘢𝘨𝘪𝘰𝘯𝘦 {season} della 𝘴𝘦𝘳𝘪𝘦 '{anime}' non esiste nella 𝗧𝗮𝗯𝗲𝗹𝗹𝗮 𝗗𝗶 𝗖𝗼𝗻𝘃𝗲𝗿𝘀𝗶𝗼𝗻𝗲."
ANIME_INEXISTENT_LOG = "❌ La 𝘴𝘦𝘳𝘪𝘦 '{anime}' non esiste nella 𝗧𝗮𝗯𝗲𝗹𝗹𝗮 𝗗𝗶 𝗖𝗼𝗻𝘃𝗲𝗿𝘀𝗶𝗼𝗻𝗲."
TABLE_INEXISTENT_LOG = "⚠️ Il file table.json non esiste, quindi verrà creato."
ANIME_RESEARCH_LOG = "🔎 Ricerca anime '{anime}' stagione {season}."
EPISODE_RESEARCH_LOG = "🔎 Ricerca episodio {episode}."
CHECK_EPISODE_AVAILABILITY_LOG = "⚙️ Verifica se l'episodio 𝐒{season}𝐄{episode} è disponibile."
EPISODE_AVAILABLE_LOG = "✔️ L'episodio è disponibile."
EPISODE_UNAVAILABLE_LOG = "✖️ L'episodio NON è ancora uscito."
EPISODE_DOWNLOAD_LOG = "⏳ Download episodio 𝐒{season}𝐄{episode}."
DOWNLOAD_COMPLETED_LOG = "✔️ Dowload Completato."
FOLDER_CREATION_LOG = "⚠️ La cartella {folder} è stata creata."
EPISODE_SHIFT_LOG = "⏳ Spostamento episodio 𝐒{season}𝐄{episode} in {folder}."
EPISODE_SHIFT_DONE_LOG = "✔️ Episodio spostato."
ANIME_REFRESH_LOG = "⏳ Ricaricando la serie '{anime}'."
EPISODE_RENAME_LOG = "⏳ Rinominando l'episodio."
EPISODE_RENAME_DONE_LOG = "✔️ Episodio rinominato."
EPISODE_RENAME_ERROR_LOG = "⚠️ NON è stato possibile rinominare l'episodio."
SEND_CONNECTION_MESSAGE_LOG = "✉️ Inviando il messaggio tramite 𝗰𝗼𝗻𝗻𝗲𝗰𝘁𝗶𝗼𝗻𝘀."
NO_EPISODES = "💤 Nessun episodio da cercare."
EPISODE_ALREADY_IN_DOWNLOADING_LOG = "🔒 L'episodio è già in download su Sonarr."

AUTOMATIC_LINK_SEARCH_LOG = "⚠️ Ricerca automatica link di AnimeWorld per la 𝘴𝘵𝘢𝘨𝘪𝘰𝘯𝘦 {season} della 𝘴𝘦𝘳𝘪𝘦 '{anime}'."
ABSOLUTE_AUTOMATIC_LINK_SEARCH_ERROR_LOG = "⛔ La ricerca automatica link di AnimeWorld è incompatibile con le serie ad ordinamento assoluto."
SPECIAL_AUTOMATIC_LINK_SEARCH_ERROR_LOG = "⛔ La ricerca automatica link di AnimeWorld è incompatibile con gli Special (Stagione 0)."
NO_RESULT_LOG = "⛔ Nessun risultato trovato."
LINK_FOUND_LOG = """✳️ Risultato trovato: 
- {anime} ({link})."""
CONNECTION_LINK_FOUND_LOG = """*Auto Ricerca Link*
Risultato trovato per _{sanime}_ _{sseason}_:
- `{anime}` ({link})."""

WARNING_STATE_LOG = "⚠️ {warning}"
ERROR_STATE_LOG = "\033[93m🆆🅰🆁🅽🅸🅽🅶: {error}\033[0m"
CRITICAL_STATE_LOG = "\033[91m🅰🅻🅴🆁🆃: {critical}\033[0m"
EXCEPTION_STATE_LOG = "\033[4;3;91m🅴🆁🆁🅾🆁: {exception}\033[0m"

CONNECTION_MESSAGE = """*Episode Downloaded*
{title} - {season}x{episode} - {episodeTitle}"""

UPDATE_CONTAINER = """🎉 È disponibile una nuova versione del container ({version})!
- Per maggiori informazioni: https://github.com/MainKronos/Sonarr-AnimeDownloader/releases/latest
"""

