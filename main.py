import os
import json
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8910485378:AAFwtDWymna3uXi1q7s4_E6ZJT198dXAFzk"

DATA_FILE = "data.json"

TYT_MAT = ["Problemler", "Sayılar", "Kümeler", "Temel Kavramlar"]
TYT_TURKCE = ["Paragraf", "Anlam", "Dil Bilgisi"]
AYT = ["Fonksiyon", "Trigonometri", "Polinom"]
EDEB = ["Şiir", "Yazar-Eser", "Edebi Akımlar"]

def load():
    try:
        return json.load(open(DATA_FILE, "r"))
    except:
        return {"done": [], "net": {}}

def save(data):
    json.dump(data, open(DATA_FILE, "w"))

def pick(topic_list, done):
    for t in topic_list:
        if t not in done:
            return t
    return random.choice(topic_list)

def make_plan(data):
    done = data["done"]

    return f"""
🤖 KOÇ AKILLI PLAN

📚 TYT MAT: {pick(TYT_MAT, done)}
📖 TYT TÜRKÇE: {pick(TYT_TURKCE, done)}
📚 AYT: {pick(AYT, done)}
📖 EDEB: {pick(EDEB, done)}

🏋️ SPOR:
- 3x15 squat
- 10 şınav
- 1 dk plank

🍳 YEMEK:
- yumurta + süt + ekmek

⏰ ÇALIŞMA: 50 dk + 10 dk mola
"""

# -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 KOÇ AKTİF! /plan yaz")

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load()
    await update.message.reply_text(make_plan(data))

# -------------------

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load()

    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /done mat Problemler")
        return

    konu = " ".join(context.args[1:])

    if konu not in data["done"]:
        data["done"].append(konu)

    save(data)
    await update.message.reply_text(f"✔ {konu} tamamlandı")

# -------------------

async def net(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load()

    if len(context.args) < 3:
        await update.message.reply_text("Kullanım: /net mat 25")
        return

    ders = context.args[1]
    net = context.args[2]

    data["net"][ders] = net
    save(data)

    await update.message.reply_text(f"📊 {ders} net: {net}")

# -------------------

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    data = load()

    if "ne yapayım" in text or "plan" in text:
        await update.message.reply_text(make_plan(data))

    elif "yoruldum" in text:
        await update.message.reply_text("KOÇ: Dinlen ama bırakma 💪")

    elif "motivasyon" in text:
        await update.message.reply_text("🔥 KOÇ: Bugün 1 saat bile çalışsan fark atarsın!")

    else:
        await update.message.reply_text("KOÇ: /plan yaz veya 'ne yapayım KOÇ' de")

# -------------------

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(CommandHandler("done", done))
app.add_handler(CommandHandler("net", net))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
