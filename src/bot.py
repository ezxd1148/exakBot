'''
Unrefined Baseline for exakBot.src.bot (Ugly)

- Today's goal: make it work (Done)
'''

# import libraries

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# loads .env from current directory

load_dotenv()

## env config

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in Environment Variable")

# main 

## functions

async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        '''
        Welcome to exakbot.
Paste a link you don’t trust, and I’ll tell you how sketchy it looks.

Send one of these:

A link (example: https://…)

A forwarded message containing a link

I’ll reply with a risk score, the real destination after redirects, and the main red flags.
If it looks risky, I’ll also tell you what to do next.

Triage only. No “100% safe” promises, because reality doesn’t work like that.
        '''
    )

## bot setup
app = ApplicationBuilder().token(TOKEN).build() # REMINDER TO CHANGE TO ENV (Done)

### command handlers

app.add_handler(CommandHandler("start", start_bot))

### run bot
app.run_polling()