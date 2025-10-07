from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carica le chiavi dal file .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

# --- Messaggi del bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 Come funziona", callback_data="funziona")],
        [InlineKeyboardButton("💰 Attivazione & Capitale", callback_data="attivazione")],
        [InlineKeyboardButton("📈 Performance Pack", callback_data="performance")],
        [InlineKeyboardButton("🔐 Sicurezza & API", callback_data="sicurezza")],
        [InlineKeyboardButton("📞 Contatti", callback_data="contatti")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Benvenuto in *Ultima Trading Bot*!\n\nScegli un argomento per scoprire di più 👇",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# --- Risposte ai pulsanti ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    risposta = ""

    if query.data == "funziona":
        risposta = (
            "🤖 *Come funziona*\n\n"
            "Ultima Trading Bot lavora con intelligenza artificiale su coppie **UCN/USDT** e **BTC/USDT**, "
            "sfruttando algoritmi di grid trading ottimizzati per generare profitto automatico. "
            "Il sistema non vende mai in perdita e segue la strategia ufficiale di UTrading su UChain."
        )

    elif query.data == "attivazione":
        risposta = (
            "💰 *Attivazione & Capitale*\n\n"
            "1️⃣ Scegli il valore del bot: da 110€ a 110.000€.\n"
            "2️⃣ Deposita almeno la stessa cifra in USDT su MEXC o BingX (fondi tuoi e sempre sotto controllo).\n"
            "3️⃣ Scegli il *Performance Pack* e la coppia di monete (UCN/USDT o BTC/USDT).\n"
            "4️⃣ Collega le API e il bot inizia a lavorare automaticamente!"
        )

    elif query.data == "performance":
        risposta = (
            "📈 *Performance Pack*\n\n"
            "I Performance Pack definiscono il rendimento e la durata del lavoro del bot. "
            "Puoi scegliere pacchetti da 11€ a 110.000€, con percentuali variabili in base al livello. "
            "Ogni pack è indipendente e puoi attivarne più di uno contemporaneamente."
        )

    elif query.data == "sicurezza":
        risposta = (
            "🔐 *Sicurezza & API*\n\n"
            "Il bot opera tramite API personali: questo significa che non trasferisci mai i tuoi fondi. "
            "Il controllo rimane sempre tuo, sul tuo account MEXC o BingX. "
            "Puoi disattivare le API in qualsiasi momento per la massima sicurezza."
        )

    elif query.data == "contatti":
        risposta = (
            "📞 *Contatti ufficiali*\n\n"
            "🌐 Sito: https://mauriziocasalin.com/trading-automatico-con-intelligenza-artificiale/\n"
            "💬 Telegram: https://t.me/Ultima_Official_Italian\n"
            "✉️ Email: info@mauriziocasalin.com\n"
            "🔗 Iscriviti: https://ultima-business.com/it/partner/s1viygb3"
        )

    await query.edit_message_text(text=risposta, parse_mode="Markdown")

# --- Avvio del bot ---
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
