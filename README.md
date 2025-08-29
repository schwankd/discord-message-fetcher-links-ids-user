# Discord Message Link Generator Bot

Dieses Projekt ist ein **Discord-Bot**, der Nachrichten aus einem oder mehreren Text-Channels ausliest und **für jede Nachricht einen direkten Discord-Link** erstellt.
Gebastelt um ein Inhaltsverzeichnis oder eine Referenzliste für Server-Nachrichten zu bauen.

---

## Features

* Liest alle Nachrichten aus angegebenen Text-Channels
* Generiert **Discord-Nachrichten-Links**
  (`https://discord.com/channels/{guild_id}/{channel_id}/{message_id}`)
* Speichert die Daten in einer **CSV-Datei** mit folgenden Spalten:

  * Channel
  * Message ID
  * Author
  * Message Text
  * Discord Message Link
* Unterstützt **mehrere Channels**

---

## Voraussetzungen

* Python 3.10+
* `discord.py` Paket
* Ein Discord-Bot mit **Token** und Berechtigungen:

  * Read Messages/View Channels
  * Read Message History

---

## Installation

1. Repository klonen oder ZIP herunterladen:

```bash
git clone https://github.com/DEIN_USER/discord-message-link-bot.git
cd discord-message-link-bot
```

2. Virtuelle Umgebung erstellen (optional, empfohlen):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Abhängigkeiten installieren:

```bash
pip install discord.py
```

---

## Bot einrichten

1. **Bot erstellen** im [Discord Developer Portal](https://discord.com/developers/applications).
2. **Token kopieren** → wird später ins Skript eingefügt.
3. **Bot auf deinen Server einladen**:

   * OAuth2 → URL Generator → Scope: `bot`
   * Berechtigungen: `Read Messages/View Channels`, `Read Message History` ´Privileged Gateway Intents - Message Content Intent´
   * URL öffnen → Server auswählen → Autorisieren

---

## Konfiguration

Im Skript `linkscraper.py` eintragen:

```python
TOKEN = "DEIN_BOT_TOKEN"  # Bot Token
CHANNEL_IDS = [123456789012345678, 987654321098765432]  # IDs der Text-Channels
```

* Channel-IDs findest du in Discord → Rechtsklick auf Channel → „ID kopieren“ (Entwicklermodus aktivieren).
* Die Message-Links haben das Format:

```
https://discord.com/channels/<GuildID>/<ChannelID>/<MessageID>
```

---

## Nutzung

Bot starten:

```bash
python3 linkscraper.py
```

* Der Bot liest alle Nachrichten aus den angegebenen Channels.
* Ergebnis: `discord_message_links.csv` im Projektordner.
* CSV enthält die **Discord-Message-Links + Infos zu Channel, Nachricht und Autor**.

---

## Hinweise

* Bot benötigt **keine Admin-Rechte**, nur Lesezugriff auf die Channels.
* Es werden **keine Links aus Text extrahiert**, sondern **direkte Nachrichten-Links erstellt**.
* Den Token **niemals veröffentlichen** oder in öffentliche Repositories hochladen.

---

## Lizenz

Dieses Projekt ist **MIT-lizenziert**.
Du kannst es frei verwenden und anpassen.
