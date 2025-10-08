from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters
from telegram.constants import ParseMode
from openai import OpenAI
from dotenv import load_dotenv
import os

# ====== CONFIG ======
load_dotenv()  # in Render non serve ma non fa danni
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
client = OpenAI()  # legge OPENAI_API_KEY dall'ambiente

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN non impostato nell'ambiente.")

# ====== TESTI ======
DISCLAIMER = (
    "\n\n⚠️ *Disclaimer*: questo bot è informativo. Nessuna garanzia di risultato. "
    "I fondi restano sempre sul tuo conto; usa API con permessi di trading soltanto."
)

TXT_FUNZIONA = (
    "🤖 *Come funziona*\n\n"
    "• UTrading Bot usa una logica di grid trading su **UCN/USDT** e **BTC/USDT**.\n"
    "• Acquisti un *Performance Pack* (in UCN) che definisce il profit limit operativo.\n"
    "• Colleghi le *API personali* (MEXC/BingX) con soli permessi di trading.\n"
    "• Il bot lavora 24/7 e si ferma quando raggiunge il profit limit."
    + DISCLAIMER
)

TXT_ATTIVAZIONE = (
    "💰 *Attivazione & Capitale*\n\n"
    "1) *Scegli il valore del bot*: da **110€** a **110.000€**.\n"
    "2) *Deposita il capitale operativo* in USDT sul tuo conto **MEXC** o **BingX** (almeno pari al valore scelto).\n"
    "   Il capitale resta sempre sul tuo conto.\n"
    "3) *Seleziona Performance Pack* e la coppia (**UCN/USDT** o **BTC/USDT**).\n"
    "4) *Collega le API* (permessi: trading only) e il bot parte in autonomia."
    + DISCLAIMER
)

TXT_PACKS = (
    "📈 *Performance Pack*\n\n"
    "• Ogni pack definisce il *profit limit* massimo.\n"
    "• Pack acquistabili in *UCN*, da 11€ a 110.000€.\n"
    "• Puoi attivare più bot in parallelo e monitorare tutto in tempo reale."
    + DISCLAIMER
)

TXT_SICUREZZA = (
    "🔐 *Sicurezza & API*\n\n"
    "• Il bot *non ha accesso ai prelievi*.\n"
    "• Usa 2FA e password robuste; limita i permessi a 'spot trading'.\n"
    "• Puoi disattivare le API in qualsiasi momento."
    + DISCLAIMER
)

TXT_CONTATTI = (
    "📞 *Contatti ufficiali*\n\n"
    "• Canale: https://t.me/Ultima_Official_Italian\n"
    "• Email: info@mauriziocasalin.com\n"
    "• Sito: https://mauriziocasalin.com/trading-automatico-con-intelligenza-artificiale/\n"
    "• Iscrizione: https://ultima-business.com/it/partner/s1viygb3"
)

TXT_FALLBACK = (
    "😕 Al momento non riesco a ottenere una risposta dall’AI. "
    "Riprova tra poco oppure usa il menu qui sotto 👇"
)

# ====== UI ======
def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🤖 Come funziona", callback_data="funziona")],
        [InlineKeyboardButton("💰 Attivazione & Capitale", callback_data="attivazione")],
        [InlineKeyboardButton("📈 Performance Pack", callback_data="performance")],
        [InlineKeyboardButton("🔐 Sicurezza & API", callback_data="sicurezza")],
        [InlineKeyboardButton("📞 Contatti", callback_data="contatti")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== AI ======
async def ai_answer(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.4,
            messages=[
                {"role": "system", "content":
                 "Sei l'assistente ufficiale di Ultima Trading Bot. "
                 "Rispondi in italiano, con tono amichevole e chiaro. "
                 "Concentrati su funzionamento, attivazione, sicurezza, packs. "
                 "Evita termini regolamentati; niente garanzie."},
                {"role": "user", "content": prompt}
            ],
        )
        return completion.choices[0].message.content
    except Exception:
        return TXT_FALLBACK

# ====== HANDLERS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Benvenuto in *Ultima Trading Bot*!\nScegli un argomento 👇",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=main_menu()
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 *Comandi*\n"
        "/start – Avvia il bot\n"
        "/menu – Mostra il menu\n"
        "/help – Elenco comandi\n"
        "/stop – Chiudi la sessione",
        parse_mode=ParseMode.MARKDOWN
    )

async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Menu principale 👇", reply_markup=main_menu())

async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Sessione terminata. Torna con /start quando vuoi.")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    mapping = {
        "funziona": TXT_FUNZIONA,
        "attivazione": TXT_ATTIVAZIONE,
        "performance": TXT_PACKS,
        "sicurezza": TXT_SICUREZZA,
        "contatti": TXT_CONTATTI,
    }
    text = mapping.get(data)
    if text:
        await q.message.edit_text(text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = (update.message.text or "").lower()
    if "funzion" in t:
        await update.message.reply_text(TXT_FUNZIONA, parse_mode=ParseMode.MARKDOWN)
    elif "attiv" in t or "capitale" in t:
        await update.message.reply_text(TXT_ATTIVAZIONE, parse_mode=ParseMode.MARKDOWN)
    elif "pack" in t or "licenz" in t or "performance" in t:
        await update.message.reply_text(TXT_PACKS, parse_mode=ParseMode.MARKDOWN)
    elif "sicurez" in t or "api" in t:
        await update.message.reply_text(TXT_SICUREZZA, parse_mode=ParseMode.MARKDOWN)
    elif "contatt" in t or "support" in t:
        await update.message.reply_text(TXT_CONTATTI, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    else:
        reply = await ai_answer(update.message.text)
        await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

# ====== BOOT ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
    print("✅ Ultima Trading Bot avviato. In ascolto…")
    app.run_polling()

if __name__ == "__main__":
    main()
