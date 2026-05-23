"""
diary-bot.py — Telegram bot for diary study entry intake.
Input: text messages, photos, voice notes from participants.
Output: JSONL entries in entries.jsonl, media files in media/.

Install: pip install python-telegram-bot
Run: TG_TOKEN=xxx python diary-bot.py
"""
import json
import os
import datetime
import pathlib

from telegram.ext import Application, MessageHandler, filters

LOG = pathlib.Path("entries.jsonl")
MEDIA = pathlib.Path("media")
MEDIA.mkdir(exist_ok=True)

app = Application.builder().token(os.environ["TG_TOKEN"]).build()


async def on_msg(update, ctx):
    msg = update.message
    entry = {
        "ts": datetime.datetime.utcnow().isoformat(),
        "participant_id": msg.from_user.id,
        "text": msg.text or msg.caption or "",
    }
    if msg.photo:
        f = await msg.photo[-1].get_file()
        path = str(MEDIA / f"{msg.message_id}.jpg")
        await f.download_to_drive(path)
        entry["photo"] = path
    if msg.voice:
        f = await msg.voice.get_file()
        path = str(MEDIA / f"{msg.message_id}.ogg")
        await f.download_to_drive(path)
        entry["voice"] = path
        # Transcribe locally with Whisper after the fact:
        # import whisper; model = whisper.load_model("base")
        # entry["transcript"] = model.transcribe(path)["text"]
    with LOG.open("a") as fp:
        fp.write(json.dumps(entry) + "\n")
    await msg.reply_text("Got it — thanks!")


app.add_handler(MessageHandler(filters.ALL, on_msg))
app.run_polling()
