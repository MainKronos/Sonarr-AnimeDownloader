WARNC='\033[93m' #GIALLO
ALERTC='\033[91m' # ROSSO
ERRORC='\033[4;3;91m' # ROSSO
TITLEC='\033[1;94m' # BLU
SEPARC='\033[90m' # GRIGIO
DIVIDC='\033[1;90m' # GRIGIO
OKC='\033[92m' # VERDE
NC='\033[0m' # Ripristino


START_LOG = """\033[1;94m┌-------------------------------------{time}-----------------------------------┐
\033[1;94m|                 _                _____                      _                 _            |
\033[1;94m|     /\\         (_)              |  __ \\                    | |               | |           |
\033[1;94m|    /  \\   _ __  _ _ __ ___   ___| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __  |
\033[1;94m|   / /\\ \\ | '_ \\| | '_ ` _ \\ / _ \\ |  | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |/ _ \\ '__| |
\033[1;94m|  / ____ \\| | | | | | | | | |  __/ |__| | (_) \\ V  V /| | | | | (_) | (_| | (_| |  __/ |    |
\033[1;94m| /_/    \\_\\_| |_|_|_| |_| |_|\\___|_____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\\___|_|    |
\033[1;94m|                                                                                            |
\033[1;94m└--------------------------------------------------------------------------------------------┘\033[0m"""

SONARR_URL_ERROR_LOG = "✖️ Variabile d'ambinete '𝙎𝙊𝙉𝘼𝙍𝙍_𝙐𝙍𝙇' non inserita."
SONARR_URL_CHECK_LOG = "✔ 𝙎𝙊𝙉𝘼𝙍𝙍_𝙐𝙍𝙇: {sonar_url}"

API_KEY_ERROR_LOG = "✖️ Variabile d'ambinete '𝘼𝙋𝙄_𝙆𝙀𝙔' non inserita."
API_KEY_CHECK_LOG = "✔ 𝘼𝙋𝙄_𝙆𝙀𝙔: {api_key}"

CHAT_ID_ERROR_LOG = "✖️ Variabile d'ambinete '𝘾𝙃𝘼𝙏_𝙄𝘿' non inserita."
CHAT_ID_CHECK_LOG = "✔ 𝘾𝙃𝘼𝙏_𝙄𝘿: {chat_id}"

BOT_TOKEN_ERROR_LOG = "✖️ Variabile d'ambinete '𝘽𝙊𝙏_𝙏𝙊𝙆𝙀𝙉' non inserita."
BOT_TOKEN_CHECK_LOG = "✔ 𝘽𝙊𝙏_𝙏𝙊𝙆𝙀𝙉: {bot_token}"

AMBIENT_VARS_CHECK_LOG = "\033[92m☑️ Le variabili d'ambiente sono state inserite correttamente.\033[0m"

SCAN_DELAY_LOG = "⚙️ Intervallo Scan: {delay} minuti."

START_SERVER_LOG = "✔️ Server Avviato."

DIVIDER_LOG = "\033[1;90m- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \033[0m"
START_BLOCK_LOG = "\033[90m╭-----------------------------------「{time}」-----------------------------------╮\033[0m"
END_BLOCK_LOG = "\033[90m╰-----------------------------------「{time}」-----------------------------------╯\033[0m"

ANIME_REJECTED_LOG = "⁉️ Serie '{anime}' S{season} scartata per mancanza di informazioni."

CONNECTION_ERROR_LOG = "⚠️ Errore di connessione. ({res_error})"

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
SEND_TELEGRAM_MESSAGE_LOG = "✉️ Inviando il messaggio via telegram."
NO_EPISODES = "Non c'è nessun episodio da cercare."

AUTOMATIC_LINK_SEARCH_LOG = "⚠️ Ricerca automatica link di AnimeWorld per la 𝘴𝘵𝘢𝘨𝘪𝘰𝘯𝘦 {season} della 𝘴𝘦𝘳𝘪𝘦 '{anime}'."
ABSOLUTE_AUTOMATIC_LINK_SEARCH_ERROR_LOG = "⛔ La ricerca automatica link di AnimeWorld è incompatibile con le serie ad ordinamento assoluto."
NO_RESULT_LOG = "⛔ Nessun risultato trovato."
LINK_FOUND_LOG = """✳️ Risultato trovato: 
- {anime} ({link})."""

WARNING_STATE_LOG = "⚠️ {warning}"
ERROR_STATE_LOG = "\033[93m🆆🅰🆁🅽🅸🅽🅶: {error}\033[0m"
CRITICAL_STATE_LOG = "\033[91m🅰🅻🅴🆁🆃: {critical}\033[0m"
EXCEPTION_STATE_LOG = "\033[4;3;91m🅴🆁🆁🅾🆁: {exception}\033[0m"

TELEGRAM_MESSAGE = """*Episode Downloaded*
{title} - {season}x{episode} - {episodeTitle}"""

