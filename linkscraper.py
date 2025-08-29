import discord
import csv
import re
import asyncio

TOKEN = "deinen bot token hier rein"   # Dein Bot-Token hier eintragen
CHANNEL_IDS = [1031661075193680044, 1031660963000238153, 1031660963000238154]  # Liste mit den Channel-IDs
USER_ID = "your user id" # deine user id muss hier rein

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Eingeloggt als {client.user}")
    
    processed_channels = []
    total_messages = 0
    total_files_created = 0
    
    for channel_id in CHANNEL_IDS:
        try:
            channel = client.get_channel(channel_id)
            if channel is None:
                print(f"❌ Channel mit ID {channel_id} nicht gefunden oder Bot hat keinen Zugriff")
                processed_channels.append({"name": f"Unknown Channel ({channel_id})", "status": "❌ Nicht gefunden", "messages": 0})
                continue
                
            print(f"📂 Lese Channel: {channel.name}")
            channel_links_data = []
            message_count = 0

            async for message in channel.history(limit=None):
                message_count += 1
                total_messages += 1
                
                # Discord Message Link für jede Nachricht generieren
                discord_message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                
                # Erste 20 Zeichen des Nachrichteninhalts
                message_preview = message.content[:20] if message.content else ""
                
                channel_links_data.append([
                    message.id,
                    message.author.name,
                    message_preview,
                    discord_message_link
                ])
                
                if message_count <= 3:  # Show first few as examples
                    print(f"🔗 Generiert Link für Nachricht von {message.author.name}: {discord_message_link}")
            
            # Separate CSV für diesen Channel erstellen
            safe_channel_name = re.sub(r'[<>:"/\\|?*]', '_', channel.name)
            filename = f"discord_links_{safe_channel_name}_{channel.id}.csv"
            
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["MessageID", "MessageAuthor", "MessageContent", "MessageLink"])
                writer.writerows(channel_links_data)
            
            total_files_created += 1
            processed_channels.append({"name": channel.name, "status": "✅ Erfolgreich", "messages": message_count})
            print(f"✅ Channel {channel.name}: {message_count} Nachrichten gescannt, CSV erstellt: {filename}")
            
        except discord.Forbidden:
            print(f"❌ Keine Berechtigung für Channel mit ID {channel_id}")
            processed_channels.append({"name": f"Channel {channel_id}", "status": "❌ Keine Berechtigung", "messages": 0})
        except discord.NotFound:
            print(f"❌ Channel mit ID {channel_id} nicht gefunden")
            processed_channels.append({"name": f"Channel {channel_id}", "status": "❌ Nicht gefunden", "messages": 0})
        except Exception as e:
            print(f"❌ Fehler beim Lesen von Channel {channel_id}: {e}")
            processed_channels.append({"name": f"Channel {channel_id}", "status": f"❌ Fehler: {e}", "messages": 0})

    # Discord Nachricht an User senden
    try:
        print(f"🔍 Suche User mit ID: {USER_ID}...")
        user = await client.fetch_user(USER_ID)
        if user:
            print(f"✅ User gefunden: {user.name}#{user.discriminator}")
            summary_message = f"🤖 **Discord Link Extractor - Zusammenfassung**\n\n"
            summary_message += f"📊 **Gesamtstatistik:**\n"
            summary_message += f"• Verarbeitete Nachrichten: {total_messages}\n"
            summary_message += f"• Erstellte CSV Dateien: {total_files_created}\n\n"
            summary_message += f"📂 **Channel Details:**\n"
            
            for channel_info in processed_channels:
                summary_message += f"• {channel_info['name']}: {channel_info['status']} ({channel_info['messages']} Nachrichten)\n"
            
            summary_message += f"\n✅ Alle CSV Dateien wurden erfolgreich erstellt!"
            
            try:
                await user.send(summary_message)
                print(f"📧 Zusammenfassung an User {user.name} gesendet")
            except discord.Forbidden:
                print(f"❌ Kann keine DM an {user.name} senden - DMs blockiert oder keine gemeinsamen Server")
            except Exception as dm_error:
                print(f"❌ Fehler beim Senden der DM: {dm_error}")
        else:
            print(f"❌ User mit ID {USER_ID} nicht gefunden")
    except discord.NotFound:
        print(f"❌ User mit ID {USER_ID} existiert nicht")
    except discord.HTTPException as http_error:
        print(f"❌ HTTP Fehler beim Abrufen des Users: {http_error}")
    except Exception as e:
        print(f"❌ Unbekannter Fehler beim User-Lookup: {e}")

    print(f"📁 Fertig! {total_files_created} CSV Dateien erstellt, {total_messages} Nachrichten verarbeitet")
    await client.close()

client.run(TOKEN)
